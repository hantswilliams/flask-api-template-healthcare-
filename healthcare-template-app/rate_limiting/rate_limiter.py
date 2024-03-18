from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os

load_dotenv()

def rate_limits_app(app):
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["10 per minute", "1 per second"], # this is the default for all routes
        storage_uri=os.getenv('REDIS_ENDPOINT'), # redis 
        storage_options={"password": "password"},
        strategy="fixed-window", # or "moving-window"
    )
    return limiter

