from api import api
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_login import LoginManager, login_required 
import logging
from models.models import db
from pages import register_blueprints  # Import the register_blueprints function
from util.auth.auth import load_user, log_user_activity, renew_session  
from util.config.loader import init_configs
from util.rbac.rbac import rbac
from util.rate_limiting.rate_limiter import init_app as init_limiter, limiter
from util.sentry.sentry import init_sentry

load_dotenv()

## Initialize the Flask app
app = Flask(__name__)

## Keep debugging on
app.logger.setLevel(logging.DEBUG)  # Set the desired logging level

# Initialize configurations, Sentry, Rate limting, API routes, database, flask-login
init_configs(app)
init_sentry()
init_limiter(app)
api.init_app(app)
db.init_app(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.user_loader(load_user) 

@app.before_request
def before_request_func():
    renew_session()

# Non-API Routes for the Flask app using blueprints
# Register the Blueprints using the function from pages/__init__.py
register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)
