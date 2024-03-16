from flask import Flask, jsonify, request, redirect, render_template_string
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from rbac.rbac import casbin_rbac
from auth.auth import User, users, load_user  # Import from your auth module


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'

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
        if username in users and users[username]['password'] == password:
            user = User(username)
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
def profile():
    return jsonify({"username": current_user.id})

@app.route('/data', methods=['GET'])
@login_required
@casbin_rbac()
def data():
    return jsonify({"data": "This is protected data."}) 

if __name__ == '__main__':
    app.run(debug=True)
