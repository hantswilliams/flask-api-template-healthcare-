from api import api
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect
from flask_login import LoginManager
import logging
from models.models import db
import os 
from pages import register_blueprints  # Import the register_blueprints function
from util.auth.auth import load_user, renew_session
from util.config.loader import init_configs
from util.rate_limiting.rate_limiter import init_app as init_limiter
from util.sentry.sentry import init_sentry
from werkzeug.exceptions import Forbidden
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()

## Initialize the Flask app
app = Flask(__name__)

## Keep debugging on
app.logger.setLevel(logging.DEBUG)  # Set the desired logging level

# Initialize Configurations, Sentry (logging), and Rate limting across the app
init_configs(app)
init_sentry()
init_limiter(app)

# #### TESTING SECTION
app.config["PREFERRED_URL_SCHEME"] = "https"
app.config['BASE_URL'] = os.getenv("PROD_URL_HTTPS")
app.wsgi_app = ProxyFix(app.wsgi_app)

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
    scheme = request.headers.get('X-Forwarded-Proto')
    if scheme and scheme == 'http' and request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

# Error handling for 403 Forbidden
@app.errorhandler(Forbidden)
def handle_forbidden(e):
    return render_template("403.html"), 403


# Non-API Routes for the Flask app using blueprints (pages folder - init.py)
register_blueprints(app)

# Run the app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5005)
