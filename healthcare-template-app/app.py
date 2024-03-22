from api import api
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, jsonify, request, redirect, render_template_string, render_template, url_for, session, current_app
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import logging
from models.models import db, Permission, APIToken
import pyotp
import pyqrcode
from util.auth.auth import User, load_user, validate_password, log_user_activity, renew_session  
from util.auth.auth_audit import update_login_audit_info
from util.config.loader import init_configs
from util.data_access.permissions import get_user_permissions
from util.rbac.rbac import rbac
from util.rate_limiting.rate_limiter import init_app as init_limiter, limiter
from util.sentry.sentry import init_sentry
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

## Initialize the Flask app
app = Flask(__name__)

## Keep debugging on
app.logger.setLevel(logging.DEBUG)  # Set the desired logging level

# Initialize configurations, Sentry, Rate limting, API routes, database, flask-login
init_configs(app)
init_sentry()
init_limiter(app)
api.init_app(app)
db.init_app(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.user_loader(load_user) 

@app.before_request
def before_request_func():
    renew_session()

# Non-API Routes for the Flask app
## Home Route 
@app.route('/')
def index():
    return render_template('index.html')

## Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Validate the password
        valid, message = validate_password(password)
        if not valid:
            return render_template('registration.html', message=message, username=username)

        # Continue with user creation if the password is valid
        # Remember to hash the password before storing it
        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        # Create a new token for the user
        user = User.query.filter_by(username=username).first()
        APIToken.create_token(user.id, user.username)

        return redirect(url_for('twofa', user_id=user.id))
    return render_template('registration.html')

## 2FA setup route for new user 
@app.route('/register/twofa/<int:user_id>')
def twofa(user_id):
    user = User.query.get(user_id)
    if user is None:
        return 'User not found', 404
    otpauth_url = pyotp.totp.TOTP(user.otp_secret).provisioning_uri(user.username, issuer_name='Flask Healthcare Template')
    qr_code = pyqrcode.create(otpauth_url)
    qr_code.png('static/user_{}.png'.format(user_id), scale=5)
    return render_template('twofa.html', user_id=user_id)

## 2FA setup route for admin or existing user, reset 2FA
@app.route('/register/admin/2fa/setup', methods=['GET', 'POST'])
def admin_2fa_setup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Validate the username and password
        user = User.query.filter_by(username=username).first()
        if user is None:
            return 'User not found', 404
        # Verify the password
        if user and check_password_hash(user.password, password):
            otpauth_url = pyotp.totp.TOTP(user.otp_secret).provisioning_uri(user.username, issuer_name='Flask Healthcare Template')
            qr_code = pyqrcode.create(otpauth_url)
            qr_code.png('static/user_{}.png'.format(user.id), scale=5)
            return render_template('twofa.html', user_id=user.id)
    return render_template('twofa_admin.html')

## Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    remaining_attempts = 5  # Default remaining attempts if the user or request.method is not POST

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        token = request.form['token']
        user = User.query.filter_by(username=username).first()  # Find the user by username

        # Check if account is locked
        if user and user.lockout_until and user.lockout_until > datetime.now():
            lockout_message = 'Account locked. Please try again later.'
            return render_template_string('''
                <p>{{lockout_message}}</p>
                <a href="/login">Return to Login</a>
            ''', lockout_message=lockout_message)
        
        # Calculate remaining attempts
        if user:
            remaining_attempts = max(0, 5 - user.failed_login_attempts)

        if user and check_password_hash(user.password, password):  # Verify the password

            # Check if the password has expired
            password_age = datetime.now() - user.password_changed_at
            password_expires_after = timedelta(days=90)  # Configure as needed
            
            if password_age > password_expires_after:
                # Logged them in and redirect them to the change password page
                login_user(user)
                return redirect('/change_password')  # Implement this route

            if pyotp.TOTP(user.otp_secret).verify(token):
                # Call update_login_audit_info to handle the audit info update
                update_login_audit_info(user, request.remote_addr)
                user.failed_login_attempts = 0  # Reset failed login attempts
                db.session.commit()
                login_user(user)

                return redirect('/profile')  # Redirect to a secure page after login
            
            else:
                return 'Invalid 2FA token', 403

        else:
            if user:
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= 5:  # Lockout threshold
                    user.lockout_until = datetime.now() + timedelta(minutes=15)  # Lockout period
                else:
                    remaining_attempts = max(0, 5 - user.failed_login_attempts)
                db.session.commit()
            invalid_login_message = 'Invalid username or password'
        
    # Include remaining_attempts in the template
    return render_template_string('''
        <p>{{invalid_login_message}}</p>
        <p>You have {{remaining_attempts}} remaining login attempts.</p>
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            Token: <input type="text" name="token"><br>
            <input type="submit" value="Login">
        </form>
        <p> If you need to register or re-register 2FA with your account, please click <a href="/register/admin/2fa/setup">here</a></p>
    ''', invalid_login_message=invalid_login_message if 'invalid_login_message' in locals() else '', remaining_attempts=remaining_attempts)


## Change password route
@app.route('/change_password', methods=['GET', 'POST'])
@login_required
@log_user_activity
def change_password():
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        
        user = current_user
        
        # Verify current password
        if not check_password_hash(user.password, current_password):
            return "Current password is incorrect.", 400
        
        # Validate new password strength
        valid, message = validate_password(new_password)
        if not valid:
            return render_template_string('''
                <p>{{message}}</p>
                <form method="post">
                    Current Password: <input type="password" name="current_password"><br>
                    New Password: <input type="password" name="new_password"><br>
                    <input type="submit" value="Change Password">
                </form>
            ''', message=message)
        
        # Update password and password_changed_at
        user.password = generate_password_hash(new_password)
        user.password_changed_at = datetime.now()
        db.session.commit()
        
        return redirect('/login')
    
    return render_template_string('''
        <form method="post">
            Current Password: <input type="password" name="current_password"><br>
            New Password: <input type="password" name="new_password"><br>
            <input type="submit" value="Change Password">
        </form>
    ''')

## Retrieve logged in user API token route
@app.route('/api-token')
@login_required
def my_api_token():
    user_token = APIToken.query.filter_by(username=current_user.username).first()
    if user_token:
        return jsonify({'token': user_token.token, 'last_updated': user_token.last_updated})
    return jsonify({'message': 'No API token found. Please generate one.'})

## Generate API token route
@app.route('/api-token-generate', methods=['GET'])
@login_required
def generate_api_token():
    # Attempt to find an existing token for the current user
    user_token = APIToken.query.filter_by(user_id=current_user.id).first()
    
    if user_token:
        # Update the existing token using the model's method
        user_token.update_token()
    else:
        # No existing token, so use the static method to create a new one
        APIToken.create_token(current_user.id, current_user.username)

    db.session.commit()
    return redirect('/api-token')

## Logout route
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')

## Profile route
@app.route('/profile')
@login_required
@log_user_activity
def profile():
    ## get permissions
    user_permissions = get_user_permissions(current_user.id)
    ## get user token
    user_token = APIToken.query.filter_by(username=current_user.username).first()
    if user_token:
        user_token = user_token.token
    else:
        user_token = "No token found"
    return render_template('profile.html',
                           username=current_user.username,
                           userid=current_user.id,
                           user_permissions=user_permissions,
                           user_token=user_token)

## ADMIN route for managing RBAC permissions, creating new users, deleting users, resetting passwords
@app.route('/manage-permissions')
@login_required
@log_user_activity
@rbac()
def permissions_view():
    permissions = Permission.query.all()
    users = User.query.all()

    # Generate a list of all available endpoints
    routes = []

    for i in app.url_map.iter_rules():
        if i.endpoint != 'static': # Skip the static endpoint provided by Flask
            endpoint_value = str(i).replace('<', '{').replace('>', '}')
            endpoint_value = endpoint_value.split('{')[0]
            routes.append({
                "endpoint": endpoint_value,
                "methods": list(i.methods - set(['HEAD', 'OPTIONS']))
            })

    return render_template('permissions.html', permissions=permissions, users=users, routes=routes)


## TO UPDATE: this route below should probably move over to the api folder and be part of a name space
@app.route('/permissions', methods=['POST', 'GET'])
@login_required
@log_user_activity
@limiter.exempt # this route is exempt from the default limits
def manage_permissions():
    if request.method == 'POST':
        data = request.get_json()
        ## query the subject to return their user_id
        user = User.query.filter_by(username=data['subject']).first()
        new_permission = Permission(
            user_id=user.id,
            subject=data['subject'], 
            object=data['object'], 
            action=data['action'])
        db.session.add(new_permission)
        db.session.commit()
        return jsonify({"message": "Permission created"}), 201  # Return a JSON response

    if request.method == 'GET':
        permissions = Permission.query.all()
        permissions_list = [{"id": p.id, "user_id": p.user_id, "subject": p.subject, "object": p.object, "action": p.action} for p in permissions]
        return jsonify(permissions_list), 200
    
## TO update: get a individual users list of permissions, should also move to a namespace in the api folder
@app.route('/permissions/<int:user_id>', methods=['GET'])
@login_required
def user_permission(user_id):
    permissions = get_user_permissions(user_id)
    return jsonify(permissions), 200


## TO UPDATE: list of users , should also move to a namespace in the api folder
@app.route('/subjects')
@login_required
def get_subjects():
    subjects = [user.username for user in User.query.all()]
    return jsonify(subjects), 200

## TO UPDATE: to update permissions, should also move to a namespace in the api folder
@app.route('/permissions/<int:permission_id>', methods=['PUT', 'DELETE'])
@login_required
def modify_permission(permission_id):
    permission = Permission.query.get_or_404(permission_id)

    if request.method == 'PUT':
        # Update existing Permission
        data = request.get_json()
        permission.user_id = data.get('user_id', permission.user_id)
        permission.subject = data.get('subject', permission.subject)
        permission.object = data.get('object', permission.object)
        permission.action = data.get('action', permission.action)
        db.session.commit()
        return jsonify({"message": "Permission updated"}), 200

    elif request.method == 'DELETE':
        # Delete a Permission
        db.session.delete(permission)
        db.session.commit()
        return jsonify({"message": "Permission deleted"}), 200

## TO UPDATE: add users, should also move to a namespace in the api folder
@app.route('/add-user', methods=['POST'])
@login_required
def add_user():
    # Extract user details from form data or JSON
    username = request.form.get('username')
    password = request.form.get('password')
    # Implement validation as needed
    
    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    # Now create a new token for the user
    new_user = User.query.filter_by(username=username).first()
    ## then create the token
    APIToken.create_token(new_user.id, new_user.username)
    return redirect(url_for('permissions_view'))

## TO UPDATE: edit users, should also move to a namespace in the api folder
@app.route('/edit-user/<int:user_id>', methods=['POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    # For simplicity, only updating password here
    new_password = request.form.get('new_password')
    user.password = generate_password_hash(new_password)
    db.session.commit()
    return redirect(url_for('permissions_view'))

## TO UPDATE: delete users, should also move to a namespace in the api folder
@app.route('/delete-user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('permissions_view'))

## Documentation page in REDOC style, the other page can be found at /swagger
@app.route('/redoc')
def redoc():
    return '''
    <!DOCTYPE html>
    <html>
      <head>
        <title>ReDoc</title>
        <!-- Redoc's latest version CDN -->
        <script src="https://cdn.jsdelivr.net/npm/redoc/bundles/redoc.standalone.js"></script>
      </head>
      <body>
        <redoc spec-url='/api/swagger.json'></redoc>
        <script>
          Redoc.init('/api/swagger.json')
        </script>
      </body>
    </html>
    '''



##################### TESTING ROUTES #####################
##################### TESTING ROUTES #####################

@app.route('/session-time-left')
@login_required
@limiter.exempt # this route is exempt from the default limits
def session_time_left():
    if 'expires_at' in session:
        expires_at = datetime.fromtimestamp(session['expires_at'])
        time_left = expires_at - datetime.now()
        return jsonify({'time_left': time_left.total_seconds()})
    else:
        return jsonify({'error': 'Session does not exist or has expired'}), 400

# create error check page for sentry
@app.route('/error')
@login_required
@rbac()
@limiter.exempt # this route is exempt from the default limits
def error():
    division_by_zero = 1 / 0
    return division_by_zero

# create a error that includes PII or PHI for sentry, that the pre-send filter will catch
@app.route('/error-PII')
@limiter.exempt # this route is exempt from the default limits
def error_PII():
    division_by_zero = "My social security number is 123-45-6789" / 0
    return division_by_zero 

# rate limit example of one per day
@app.route('/error/slow')
@limiter.limit("1 per day")
def slow():
    return "slow return - one per day"

## Data route for TESTING purposes of log, user activity, and role based access control
@app.route('/data', methods=['GET'])
@login_required
@log_user_activity
@rbac()
def data():
    return jsonify({"data": "This is protected data."}) 




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)
