from datetime import datetime
from flask import Blueprint, render_template_string, request, redirect
from flask_login import login_required, current_user
from models.models import db
from util.auth.auth import validate_password, log_user_activity  
from werkzeug.security import generate_password_hash, check_password_hash

# Create a Blueprint
changepassword_pages = Blueprint('changepassword_pages', __name__)

## Change password route
@changepassword_pages.route('/', methods=['GET', 'POST'])
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