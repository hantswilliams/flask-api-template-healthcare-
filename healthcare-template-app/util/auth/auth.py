from datetime import datetime
from functools import wraps
from flask import request, session
from flask_login import current_user
from flask import current_app  # Import this to access your app's configuration
from models.models import db, User, UserActivityLog  # Import the User and UserActivityLog models
import re

# User loader
def load_user(user_id):
    return User.query.get(int(user_id))

def renew_session():
    session['expires_at'] = (datetime.now() + current_app.config['PERMANENT_SESSION_LIFETIME']).timestamp()

def validate_password(password, **kwargs):
    # Determine the minimum password length from configuration or kwargs
    min_password_length = kwargs.get('min_password_length', current_app.config.get('PASSWORD_MIN_LENGTH', 8))
    pass_req_uppercase = kwargs.get('pass_req_uppercase', current_app.config.get('PASSWORD_REQ_UPPERCASE', True))
    pass_req_lowercase = kwargs.get('pass_req_lowercase', current_app.config.get('PASSWORD_REQ_LOWERCASE', True))
    pass_req_digital = kwargs.get('pass_req_digital', current_app.config.get('PASSWORD_REQ_DIGIT', True))
    pass_req_special = kwargs.get('pass_req_special', current_app.config.get('PASSWORD_REQ_SPECIAL', True))

    if len(password) < min_password_length:
        return False, f"Password must be at least {min_password_length} characters long."
    
    if pass_req_uppercase and not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    else:
        pass
    
    if pass_req_lowercase and not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    else:
        pass
    
    if pass_req_digital and not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."
    else:
        pass
    
    if pass_req_special and not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."
    else:
        pass
    
    return True, "Password is strong."


def log_user_activity(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            log = UserActivityLog(
                user_id=current_user.id,
                username=current_user.username,
                endpoint=request.path,
                method=request.method
            )
            db.session.add(log)
            db.session.commit()
        
        return f(*args, **kwargs)
    
    return decorated_function
