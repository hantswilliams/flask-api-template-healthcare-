from functools import wraps
from flask import request, g, current_app
from flask_login import current_user
from models.models import Permission
from werkzeug.exceptions import Unauthorized, Forbidden

def rbac():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Use the username from Flask's global `g` if available
            user = getattr(g, 'username', None) or getattr(current_user, 'username', None)

            current_app.logger.debug(f'Current user found via RBAC decorator: {user}')
            
            if not user:
                raise Unauthorized("Access denied. No valid user identified.")
            
            # Extract the HTTP method(s) from the request
            methods = request.method.split()
            
            # Check permissions for each method
            for method in methods:
                # Query the Permission model for a matching permission entry
                permission_exists = Permission.query.filter_by(
                    subject=str(user),  # Ensure the user is represented as a string if your model expects it
                    object=request.path,
                    action=method
                ).first() is not None

                # If permission is not found for any method, deny access
                if not permission_exists:
                    raise Forbidden("You do not have permission to access this resource.")
            
            # If all checks pass, call the original function
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
