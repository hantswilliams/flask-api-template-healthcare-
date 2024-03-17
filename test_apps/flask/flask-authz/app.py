from flask import Flask, jsonify, request, redirect, render_template_string, render_template
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from rbac.rbac import casbin_rbac
from auth.auth import User, load_user  # Import from your auth module
from datetime import timedelta
from models.models import db, Permission

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key' # for session management
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)  # session timeout
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db' # Example using SQLite

db.init_app(app)


# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.user_loader(load_user) ## loads fake users from local storage

@app.route('/')
def index():
    return "Welcome to the Flask-AuthZ app!"

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()  # Adjust as needed for password hashing
        if user:
            login_user(user)
            return redirect('/data')
        return 'Invalid username or password'
    return render_template_string('''
        <form method="post">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    ''')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/profile')
@login_required
@casbin_rbac()
def profile():
    return jsonify({"userid": current_user.id, "username": current_user.username})

@app.route('/data', methods=['GET'])
@login_required
@casbin_rbac()
def data():
    return jsonify({"data": "This is protected data."}) 

@app.route('/manage-permissions')
@login_required
@casbin_rbac()
def permissions_view():
    permissions = Permission.query.all()

    # Generate a list of all available endpoints
    routes = []
    for rule in app.url_map.iter_rules():
        # Skip the static endpoint provided by Flask
        if rule.endpoint != 'static':
            routes.append({
                "endpoint": rule.endpoint,
                "methods": list(rule.methods - set(['HEAD', 'OPTIONS']))
            })

    return render_template('permissions.html', permissions=permissions, routes=routes)

@app.route('/permissions', methods=['POST', 'GET'])
@login_required
def manage_permissions():
    if request.method == 'POST':
        data = request.get_json()
        new_permission = Permission(subject=data['subject'], object=data['object'], action=data['action'])
        db.session.add(new_permission)
        db.session.commit()
        return jsonify({"message": "Permission created"}), 201  # Return a JSON response

    if request.method == 'GET':
        permissions = Permission.query.all()
        permissions_list = [{"id": p.id, "subject": p.subject, "object": p.object, "action": p.action} for p in permissions]
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


if __name__ == '__main__':
    app.run(debug=True)
