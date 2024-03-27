from datetime import datetime
from flask import Blueprint, jsonify, session
from flask_login import login_required
from util.rate_limiting.rate_limiter import limiter

# Create a Blueprint
session_time = Blueprint("session_time", __name__)


@session_time.route("/")
@login_required
@limiter.exempt  # this route is exempt from the default limits
def session_time_left():
    if "expires_at" in session:
        expires_at = datetime.fromtimestamp(session["expires_at"])
        time_left = expires_at - datetime.now()
        return jsonify(
            {
                "remaining time: ": time_left.total_seconds(),
                "working explanation": "This route tells you how many seconds are left in the current session; refresh the page to see the time left gets reset after each request, which keeps the session alive whenever there is a GET, POST, PUT, DELETE, etc. request",
            }
        )
    else:
        return jsonify({"error": "Session does not exist or has expired"}), 400
