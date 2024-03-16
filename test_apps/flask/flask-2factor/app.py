from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import pyotp
import pyqrcode
import os
import base64

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./twofa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    otp_secret = db.Column(db.String(16))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.otp_secret is None:
            # Generate a random secret for each new user
            self.otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')

# Ensure the Flask application context is available before creating the database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('twofa', user_id=user.id))
    return render_template('register.html')

@app.route('/twofa/<int:user_id>')
def twofa(user_id):
    user = User.query.get(user_id)
    if user is None:
        return 'User not found', 404
    otpauth_url = pyotp.totp.TOTP(user.otp_secret).provisioning_uri(user.username, issuer_name='Your App')
    qr_code = pyqrcode.create(otpauth_url)
    qr_code.png('static/user_{}.png'.format(user_id), scale=5)
    return render_template('twofa.html', user_id=user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        token = request.form['token']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            if pyotp.TOTP(user.otp_secret).verify(token):
                session['user_id'] = user.id
                session['username'] = user.username
                return redirect(url_for('success'))
            else:
                return 'Invalid token', 403
        else:
            return 'Invalid credentials', 403
    return render_template('login.html')

@app.route('/success')
def success():
    print('Session: ', session)
    return render_template('success.html', user_id=session['user_id'], username=session['username'])

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
