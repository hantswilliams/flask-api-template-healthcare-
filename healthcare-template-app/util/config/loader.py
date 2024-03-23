from dotenv import load_dotenv
from datetime import timedelta
import os
import yaml
from werkzeug.middleware.proxy_fix import ProxyFix

def load_configurations(app):

    load_dotenv()

    # Load environment-based configurations
    env_config = {
        'SECRET_KEY': os.getenv('SECRET_KEY'),
        'SQLALCHEMY_DATABASE_URI': os.getenv('SQLALCHEMY_DATABASE_URI'),
    }

    # Determine configuration file based on environment
    config_file = 'configProd.yaml' if os.getenv('PRODUCTION_ENV') == 'True' else 'configDev.yaml'
    
    with open(config_file, 'r') as file:
        print(f'Current Environment: {"Production" if os.getenv("PRODUCTION_ENV") == "True" else "Development"}')
        file_config = yaml.safe_load(file)
        print('Configuration Loaded: ', file_config)

    # Merge file configurations into the app.config
    for key, value in file_config.items():
        app.config[key.upper()] = value

    # Merge environment-specific configurations into the app.config
    for key, value in env_config.items():
        if value is not None:
            app.config[key] = value

    # Post-processing for specific configurations
    # Convert PERMANENT_SESSION_LIFETIME and REMEMBER_COOKIE_DURATION from int (minutes or days) to timedelta
    if 'PERMANENT_SESSION_LIFETIME' in app.config:
        app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=int(app.config['PERMANENT_SESSION_LIFETIME']))
        
    if 'REMEMBER_COOKIE_DURATION' in app.config:
        app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=int(app.config['REMEMBER_COOKIE_DURATION']))

def init_configs(app):
    load_configurations(app)

    # if the PROXY_FIX config is set to True, we will use the ProxyFix middleware
    if app.config.get('PROXY_FIX'):
        app.wsgi_app = ProxyFix(app.wsgi_app)

    return app