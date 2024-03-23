from datetime import datetime
from flask import Blueprint, render_template, request, redirect
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
    message = None  # Initialize message variable
    message_type = 'info'  # Could be 'info', 'error', or 'success'

    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        user = current_user
        
        if not check_password_hash(user.password, current_password):
            message = "Current password is incorrect."
            message_type = 'error'
        else:
            valid, validation_message = validate_password(new_password)
            if not valid:
                message = validation_message
                message_type = 'error'
            else:
                user.password = generate_password_hash(new_password)
                user.password_changed_at = datetime.now()
                db.session.commit()
                message = "Password successfully changed."
                message_type = 'success'
                return redirect('/login')  # Redirect after successful password change

    # Pass the message and message_type to the template
    return render_template('change_password.html', message=message, message_type=message_type)