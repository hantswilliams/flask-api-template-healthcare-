import secrets
from flask import request, g, current_app
from functools import wraps
from models.models import db, APIToken

authorization_token = {
    "apikey": {"type": "apiKey", "in": "header", "name": "X-API-Token"}
}


def generate_secure_token():
    return secrets.token_urlsafe()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("X-API-Token")

        current_app.logger.debug(f"X-API-Token: {token}")

        if not token:
            # Flask-RESTX can handle this tuple by converting it to a JSON response
            return {"message": "X-API-Token is missing!"}, 403

        api_token = APIToken.query.filter_by(token=token).first()

        ## if no token is found, return 403
        if not api_token:
            return {"message": "X-API-Token is invalid!"}, 403

        # print current user rertrieved from the token
        current_app.logger.debug(f"Current user: {api_token.username}")

        if not api_token.username:
            return {"message": "X-API-Token is invalid!"}, 403

        if api_token.is_token_expired():
            print(
                "Token is expired. Generating new token for user: " + api_token.username
            )
            # Update the token and commit if necessary (consider security implications)
            api_token.update_token()
            db.session.commit()
            return {
                "message": "Token is expired. Please retrieve your new token from your account by going to /api-token"
            }, 401

        # Set the username in Flask's global `g` for access in subsequent decorators or views
        g.username = api_token.username

        # Proceed with the original function
        return f(*args, **kwargs)

    return decorated
