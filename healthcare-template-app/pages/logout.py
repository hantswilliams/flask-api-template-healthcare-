from flask import Blueprint, redirect, url_for, current_app
from flask_login import login_required, logout_user

# Create a Blueprint
logout_pages = Blueprint("logout_pages", __name__)


@logout_pages.route("/", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(current_app.config['BASE_URL'], 302)
    # return redirect("/")
