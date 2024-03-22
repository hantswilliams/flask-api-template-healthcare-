import secrets
from flask import request, jsonify, g
from functools import wraps
from models.models import db, APIToken

def generate_secure_token():
    return secrets.token_urlsafe()

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-API-Token')
        if not token:
            return jsonify({'message': 'X-API-Token is missing!'}), 403

        api_token = APIToken.query.filter_by(token=token).first()
        if not api_token:
            return jsonify({'message': 'X-API-Token is invalid!'}), 403

        if api_token.is_token_expired():
            # Note: As per your requirements, regenerate the token here but don't validate this request
            api_token.update_token()
            db.session.commit()
            return jsonify({'message': 'Token is expired. Please retrieve your new token from your account.'}), 401
        
        # Set the username in Flask's global `g` for access in subsequent decorators or views
        g.username = api_token.username
        
        return f(*args, **kwargs)
    
    return decorated