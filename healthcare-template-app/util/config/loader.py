from dotenv import load_dotenv
from datetime import timedelta
from flask import request, current_app
from flask_talisman import Talisman
import os
import yaml
from werkzeug.middleware.proxy_fix import ProxyFix

def load_configurations(app):
    load_dotenv()

    # Load environment-based configurations
    env_config = {
        "SECRET_KEY": os.getenv("SECRET_KEY"),
        "SQLALCHEMY_DATABASE_URI": os.getenv("SQLALCHEMY_DATABASE_URI"),
    }

    # Determine configuration file based on environment
    config_file = (
        "configProd.yaml" if os.getenv("PRODUCTION_ENV") == "True" else "configDev.yaml"
    )

    with open(config_file, "r") as file:
        print(
            f'Current Environment: {"Production" if os.getenv("PRODUCTION_ENV") == "True" else "Development"}'
        )
        file_config = yaml.safe_load(file)
        print("Configuration Loaded: ", file_config)

    # Merge file configurations into the app.config
    for key, value in file_config.items():
        app.config[key.upper()] = value

    # Merge environment-specific configurations into the app.config
    for key, value in env_config.items():
        if value is not None:
            app.config[key] = value

    # Post-processing for specific configurations
    # Convert PERMANENT_SESSION_LIFETIME and REMEMBER_COOKIE_DURATION from int (minutes or days) to timedelta
    if "PERMANENT_SESSION_LIFETIME" in app.config:
        app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(
            minutes=int(app.config["PERMANENT_SESSION_LIFETIME"])
        )

    if "REMEMBER_COOKIE_DURATION" in app.config:
        app.config["REMEMBER_COOKIE_DURATION"] = timedelta(
            days=int(app.config["REMEMBER_COOKIE_DURATION"])
        )


# def load_talisman(app):
#     # Initialize Talisman with CSP allowing HTTPS resources
#     talisman = Talisman(app, content_security_policy=None)

#     @app.before_request
#     def before_request_func():
#         if request.endpoint in [
#             "redoc_pages.redoc",
#             "swagger_ui.swagger_ui",
#         ] or request.path.startswith("/swagger"):
#             # Disable CSP and HTTPS enforcement for specific endpoints if necessary
#             talisman.content_security_policy = None
#             talisman.force_https = False
#         else:
#             # Stricter CSP for all other endpoints, enforcing HTTPS
#             csp = {
#                 "default-src": ["'self'", "'unsafe-inline'"],
#                 "script-src": ["'self'", "'unsafe-inline'"],
#                 "style-src": ["'self'"],
#                 "img-src": ["'self'"],
#                 "connect-src": ["'self'", os.getenv("PROD_URL_HTTPS")],
#             }
#             talisman.content_security_policy = csp
#             talisman.content_security_policy_nonce_in = ["script-src"]
#             # Force HTTPS in production environments
#             talisman.force_https = os.getenv("PRODUCTION_ENV") == "True"

#     print("Talisman configured for HTTPS enforcement in production")


def load_talisman(app):
    # Initialize Talisman with a base CSP
    talisman = Talisman(app, content_security_policy=None)

    @app.before_request
    def before_request_func():
        if request.endpoint in [
            "redoc_pages.redoc",
            "swagger_ui.swagger_ui",
        ] or request.path.startswith("/swagger"):
            # Disable CSP and HTTPS enforcement for specific endpoints if necessary
            talisman.content_security_policy = None
            talisman.force_https = False
        ## if production, enforce HTTPS and CSP
        if os.getenv("PRODUCTION_ENV") == "True":
            # Stricter CSP for all other endpoints, enforcing HTTPS and using nonces #"'self'"
            csp = {
                "default-src": [current_app.config.get("BASE_URL")], 
                "script-src": [current_app.config.get("BASE_URL")],
                "style-src": [current_app.config.get("BASE_URL")],
                "img-src": [current_app.config.get("BASE_URL")],
                "connect-src": [current_app.config.get("BASE_URL")]
            }
            talisman.content_security_policy = csp
            talisman.content_security_policy_nonce_in = ["script-src"]
            talisman.force_https = os.getenv("PRODUCTION_ENV") == "True"

            ## this part below is specific, assuming production is in 
            ## a cloud environment with a load balancer, like google cloud run
            ## in the future, should modify this part depending on a preference/setting
            ## of deployment, like a config file
            app.wsgi_app = ProxyFix(app.wsgi_app) ## SHould be OFF for dev, ON for PROD

        else:
            talisman.content_security_policy = None
            talisman.force_https = False

def init_configs(app):
    load_configurations(app)
    load_talisman(app)
    return app
