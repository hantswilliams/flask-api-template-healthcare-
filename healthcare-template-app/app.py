from api import api
from dotenv import load_dotenv
from flask import Flask
from flask_login import LoginManager 
import logging
from models.models import db
from pages import register_blueprints  # Import the register_blueprints function
from util.auth.auth import load_user, renew_session  
from util.config.loader import init_configs
from util.rate_limiting.rate_limiter import init_app as init_limiter
from util.sentry.sentry import init_sentry

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

@app.before_request
def before_request_func():
    renew_session()

# Non-API Routes for the Flask app using blueprints
# We use blueprints, using the function from pages/__init__.py
register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)
