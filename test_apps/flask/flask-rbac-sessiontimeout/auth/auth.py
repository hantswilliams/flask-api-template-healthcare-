from functools import wraps
from flask import request
from flask_login import current_user
from models.models import db, User, UserActivityLog  # Import the User and UserActivityLog models
import re

# User loader
def load_user(user_id):
    return User.query.get(int(user_id))

def validate_password(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one number."
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."
    
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
