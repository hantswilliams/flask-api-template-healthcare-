# app.py

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per minute", "1 per second"], # this is the default for all routes
    storage_uri=os.getenv('REDIS_ENDPOINT'), # redis 
    storage_options={"password": "password"},
    strategy="fixed-window", # or "moving-window"
)

@app.route("/")
def index():
    return "Welcome to Flask - Limited app!"

@app.route("/slow")
@limiter.limit("1 per day")
def slow():
    return "24"

@app.route("/fast")
def fast():
    return "42"

@app.route("/ping")
@limiter.exempt # this route is exempt from the default limits
def ping():
    return 'PONG'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5005)