from datetime import datetime, timedelta
from flask import Blueprint, request, render_template_string, redirect
from flask_login import login_user
from models.models import db, User
import pyotp
from util.auth.auth_audit import update_login_audit_info
from werkzeug.security import check_password_hash

# Create a Blueprint
login_pages = Blueprint('login_pages', __name__)

## Login route
@login_pages.route('/', methods=['GET', 'POST'])
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

