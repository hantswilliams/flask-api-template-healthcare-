from flask import Blueprint, redirect
from flask_login import login_required, logout_user

# Create a Blueprint
logout_pages = Blueprint("logout_pages", __name__)


@logout_pages.route("/", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect("/")
