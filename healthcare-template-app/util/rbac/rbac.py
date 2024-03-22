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



# Casbin setup

# def casbin_rbac():
#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             # Use the username from Flask's global `g` if available
#             user = getattr(g, 'username', None) or getattr(current_user, 'username', None)
            
#             if not user:
#                 return jsonify({"error": "Access denied. No valid user identified."}), 401
            
#             path = request.path
#             methods = request.method if not hasattr(f, 'methods') else f.methods  # Gets the methods from the route or the current request
            
#             # If 'methods' is not a list (i.e., a single method string), make it a list
#             if not isinstance(methods, list):
#                 methods = [methods]
            
#             # Check permissions for each method
#             for method in methods:

#                 # Query the Permission model for a matching permission entry
#                 permission_exists = Permission.query.filter_by(
#                     subject=str(user),  # Ensure the user is represented as a string if your model expects it
#                     object=path,
#                     action=method
#                 ).first() is not None

#                 print(f"Checking permission for {user} to {method} {path}... {permission_exists}")

#                 # If permission is not found for any method, deny access
#                 if not permission_exists:
#                     return jsonify({"error": "You are either logged or provided your correct API token, but do not have access to this individual resource"}), 403
            
#             # If all checks pass, call the original function
#             return f(*args, **kwargs)
        
#         return decorated_function
#     return decorator

