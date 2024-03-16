import casbin
from functools import wraps
from flask import request, jsonify
from flask_login import current_user

# Casbin setup
e = casbin.Enforcer("rbac/model.conf", "rbac/policy.csv")

def casbin_rbac():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = current_user.id  # Assuming current_user.id gives the unique identifier of the logged-in user
            path = request.path
            methods = request.method if not hasattr(f, 'methods') else f.methods  # Gets the methods from the route or the current request
            
            # If 'methods' is not a list (i.e., a single method string), make it a list
            if not isinstance(methods, list):
                methods = [methods]
            
            # Check permissions for each method
            for method in methods:
                if not e.enforce(str(user), path, method):
                    # If any method is not allowed, return an access denied response
                    return jsonify({"error": "You are logged in, but do not have access to this individual resource"}), 403
            
            # If all checks pass, call the original function
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator