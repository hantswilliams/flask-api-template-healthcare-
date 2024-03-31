from flask import Blueprint, render_template

# Create a Blueprint
redoc_pages = Blueprint("redoc_pages", __name__)

## Redoc route
@redoc_pages.route("/")
def redoc():
    return render_template("redoc.html")
