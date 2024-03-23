from flask import Blueprint, render_template

# Create a Blueprint
landing_pages = Blueprint('landing_pages', __name__)

# Example route within your blueprint
@landing_pages.route('/')
def landing():
    return render_template('index.html')
