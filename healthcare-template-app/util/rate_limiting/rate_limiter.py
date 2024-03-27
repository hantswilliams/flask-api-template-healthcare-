from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os

load_dotenv()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["10 per minute", "1 per second"],
    storage_uri=os.getenv("REDIS_ENDPOINT"),
    storage_options={"password": os.getenv("REDIS_PASSWORD")},
    strategy="fixed-window",
)


def init_app(app):
    limiter.init_app(app)
