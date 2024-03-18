from flask import Flask, jsonify, request, redirect, render_template_string, render_template, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from rbac.rbac import casbin_rbac
from flask_restx import Resource, Namespace
from api_documentation.docs import flask_api_docs
from werkzeug.security import generate_password_hash, check_password_hash
from auth.auth import User, load_user, validate_password, log_user_activity  
from auth.auth_audit import update_login_audit_info
from auth.tokens import token_required
from rate_limiting.rate_limiter import rate_limits_app
from datetime import datetime, timedelta
from models.models import db, Permission, APIToken
from sentry.sentry import init_sentry
import pyotp
import pyqrcode


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret-key' # for session management
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)  # session timeout set to 1 minute of inactivity
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' # Example using SQLite

# Session cookie settings
app.config['SESSION_COOKIE_SECURE'] = False # Set to True for HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True # Mitigates XSS attacks
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax' # Mitigates CSRF attackss

# Remember cookie settings for Flask-Login
app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=7) # Set the remember cookie to 7 days
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=12) # Set the session lifetime to 12 hours

# Initialize Sentry
init_sentry()

# Intialize API documentation
api_docs = flask_api_docs(app)

# Initialize rate limiting
limiter = rate_limits_app(app)

db.init_app(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.user_loader(load_user) ## loads fake users from local storage

@app.route('/')
def index():
    return render_template_string('''
        <H4> Welcome to the Opionated Healthcare Flask Demo / Template App </H4>
        <p> This is a simple Flask app that demonstrates how to implement basic security measures that should always be considered when building a healthcare application. </p>
        <a href="/login">Login</a><br>
        <a href="/register">Register</a><br>
    ''')

@app.route('/register', methods=['GET', 'POST'])  # Assuming you have a registration route
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Validate the password
        valid, message = validate_password(password)
        if not valid:
            return render_template_string('''
                <p>{{message}}</p>
                <form method="post">
                    Username: <input type="text" name="username"><br>
                    Password: <input type="password" name="password"><br>
                    <input type="submit" value="Register">
                </form>
            ''', message=message)
        
        # Continue with user creation if the password is valid
        # Remember to hash the password before storing it
        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        # Create a new token for the user
        user = User.query.filter_by(username=username).first()
        APIToken.create_token(user.id, user.username)

        return redirect(url_for('twofa', user_id=user.id))
    return render_template_string('''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Register">
        </form>
    ''')

@app.route('/register/twofa/<int:user_id>')
def twofa(user_id):
    user = User.query.get(user_id)
    if user is None:
        return 'User not found', 404
    otpauth_url = pyotp.totp.TOTP(user.otp_secret).provisioning_uri(user.username, issuer_name='Flask Healthcare Template')
    qr_code = pyqrcode.create(otpauth_url)
    qr_code.png('static/user_{}.png'.format(user_id), scale=5)
    return render_template('twofa.html', user_id=user_id)

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

# Login route
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
                return redirect('/data')  # Redirect to a secure page after login
            
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


@app.route('/change_password', methods=['GET', 'POST'])
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

@app.route('/api-token')
@login_required
def my_api_token():
    user_token = APIToken.query.filter_by(username=current_user.username).first()
    if user_token:
        return jsonify({'token': user_token.token, 'last_updated': user_token.last_updated})
    return jsonify({'message': 'No API token found. Please generate one.'})

@app.route('/api-token-test', methods=['GET'])
@token_required
@casbin_rbac()
def api_token_test():
    return jsonify({'message': 'You are authorized to access this endpoint.'})

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

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/profile')
@login_required
@log_user_activity
@casbin_rbac()
def profile():
    return jsonify({"userid": current_user.id, "username": current_user.username})

@app.route('/data', methods=['GET'])
@login_required
@log_user_activity
@casbin_rbac()
def data():
    return jsonify({"data": "This is protected data."}) 

@app.route('/manage-permissions')
@login_required
@log_user_activity
@casbin_rbac()
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
    
@app.route('/subjects')
@login_required
def get_subjects():
    subjects = [user.username for user in User.query.all()]
    return jsonify(subjects), 200

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

# Add a new user
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

@app.route('/edit-user/<int:user_id>', methods=['POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    # For simplicity, only updating password here
    new_password = request.form.get('new_password')
    user.password = generate_password_hash(new_password)
    db.session.commit()
    return redirect(url_for('permissions_view'))

@app.route('/delete-user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('permissions_view'))

# create error check page for sentry
@app.route('/error')
@login_required
@casbin_rbac()
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



# @app.route('/redoc')
# def redoc():
#     return '''
#     <!DOCTYPE html>
#     <html>
#       <head>
#         <title>ReDoc</title>
#         <!-- Redoc's latest version CDN -->
#         <script src="https://cdn.jsdelivr.net/npm/redoc/bundles/redoc.standalone.js"></script>
#       </head>
#       <body>
#         <redoc spec-url='/api/swagger.json'></redoc>
#         <script>
#           Redoc.init('/api/swagger.json')
#         </script>
#       </body>
#     </html>
#     '''

## name space test 
ns_data_test = api_docs.namespace('data', description='Hello operations')
@ns_data_test.route('/test')
class DataTest(Resource):
    @casbin_rbac()
    @log_user_activity
    @limiter.limit("1 per second")
    def get(self):
        return {'hello': 'world'}




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)
