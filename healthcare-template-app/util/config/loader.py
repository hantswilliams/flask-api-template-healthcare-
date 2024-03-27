from dotenv import load_dotenv
from datetime import timedelta
from flask import request
from flask_talisman import Talisman
import os
import yaml


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


def load_talisman(app):
    # if os.getenv("PRODUCTION_ENV") == "False":
    #     print("Not a production environment, security set low r Talisman")
    #     Talisman(app, content_security_policy=None)
    #     pass
    # else:
    #     print("Production environment, True for Talisman")
    #     # Talisman(app, content_security_policy=None)
    #     csp = {
    #         "script-src": "'self'",
    #         "style-src": "'self'",
    #         "img-src": "'self'",
    #     }
    #     Talisman(
    #         app,
    #         content_security_policy=csp,
    #         content_security_policy_nonce_in=["script-src"],
    #     )
    #     print("Talisman initialized, without CSP")

    # Initialize Talisman without enforcing CSP globally
    talisman = Talisman(app, content_security_policy=None, force_https=False)

    @app.before_request
    def before_request_func():
        # Check if the request is for the 'redoc' endpoint or /swagger endpoint
        if request.endpoint == "redoc_pages.redoc" or request.path.startswith(
            "/swagger"
        ):
            # Disable CSP for 'redoc' endpoint
            talisman.content_security_policy = None
            talisman.force_https = False
        else:
            # Apply stricter CSP for all other endpoints
            csp = {
                "default-src": "'self'",
                "script-src": "'self'",
                "style-src": "'self'",
                "img-src": "'self'",
            }
            talisman.content_security_policy = csp
            talisman.content_security_policy_nonce_in = ["script-src"]
            talisman.force_https = os.getenv("PRODUCTION_ENV") == "True"

    print("Talisman configured with dynamic CSP based on request endpoint")


def init_configs(app):
    load_configurations(app)
    load_talisman(app)
    return app
