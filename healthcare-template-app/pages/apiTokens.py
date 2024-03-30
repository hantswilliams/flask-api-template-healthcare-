from flask import Blueprint, render_template, redirect, url_for, current_app
from flask_login import login_required, current_user
from models.models import db, APIToken

# Create a Blueprint
token_pages = Blueprint("token_pages", __name__)


## Retrieve logged in user API token route
@token_pages.route("/")
@login_required
def my_api_token():
    user_token = APIToken.query.filter_by(username=current_user.username).first()
    if user_token:
        # Pass the token and last_updated date to the template
        return render_template(
            "apiTokens.html",
            token=user_token.token,
            last_updated=user_token.last_updated,
        )
    # Optionally, handle the case where there is no token differently, perhaps with a message or redirect
    return render_template(
        "apiTokens.html", message="No API token found. Please generate one."
    )


## Generate API token route
@token_pages.route("/generate", methods=["GET"])
@login_required
def generate_api_token():
    user_token = APIToken.query.filter_by(user_id=current_user.id).first()

    if user_token:
        user_token.update_token()
    else:
        APIToken.create_token(current_user.id, current_user.username)

    db.session.commit()

    return redirect(url_for("token_pages.my_api_token"), 302)
