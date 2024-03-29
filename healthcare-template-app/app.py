from api import api
from dotenv import load_dotenv
from flask import Flask, render_template
from flask_login import LoginManager
import logging
from models.models import db
import os
from pages import register_blueprints  # Import the register_blueprints function
from util.auth.auth import load_user, renew_session, https_redirects
from util.config.loader import init_configs
from util.rate_limiting.rate_limiter import init_app as init_limiter
from util.sentry.sentry import init_sentry
from werkzeug.exceptions import Forbidden

load_dotenv()

## Initialize the Flask app
app = Flask(__name__)

## Keep debugging on
app.logger.setLevel(logging.DEBUG)  # Set the desired logging level

# Initialize Configurations, Sentry (logging), and Rate limting across the app
init_configs(app)
init_sentry()
init_limiter(app)

# Initialize the API endpoints
api.init_app(app)

# Initialize the database
db.init_app(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.user_loader(load_user)

# Versioning
@app.context_processor
def inject_version():
    version_file = "version.txt"
    with open(version_file, "r") as file:
        version = file.read().strip()
    return dict(version=version)

# Renew the session before each request
@app.before_request
def before_request_func():
    renew_session()
    https_redirects()

    
# Error handling for 403 Forbidden
@app.errorhandler(Forbidden)
def handle_forbidden(e):
    return render_template("403.html"), 403

# Non-API Routes for the Flask app using blueprints (pages folder - init.py)
register_blueprints(app)

# Run the app
if __name__ == "__main__":

    if os.getenv("ENVIRONMENT") == "PROD":
        app.run(
            debug=False,
            host="0.0.0.0",
            port=5005
        )

    elif os.getenv("ENVIRONMENT") == "STAGING":
        app.run(
            debug=True, 
            host="0.0.0.0", 
            port=5005, 
            ssl_context=('certificate/cert.pem', 'certificate/key.pem')
        )

    elif os.getenv("ENVIRONMENT") == "DEV":
        app.run(
            debug=True,
            host="0.0.0.0",
            port=5005
        )
        
    else:
        raise ValueError("Environment not set. Please set the ENVIRONMENT variable to either PROD, STAGING, or DEV")