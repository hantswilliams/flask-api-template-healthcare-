from flask import Blueprint, jsonify
from flask_login import login_required
from util.auth.auth import log_user_activity
from util.rbac.rbac import rbac
from util.rate_limiting.rate_limiter import limiter

# Create a Blueprint
test_pages = Blueprint("test_pages", __name__)

## For a protected route, you can use the @login_required decorator
@test_pages.route("/protected_route")
@login_required
@limiter.exempt  # this route is exempt from the default limits
def test():
    return jsonify({"test": "This is a test route"}), 200


## For logging user activity, you can use the @log_user_activity decorator
@test_pages.route("/logging_sentry")
@login_required
@limiter.exempt  # this route is exempt from the default limits
def error():
    division_by_zero = 1 / 0
    return division_by_zero


# create a error that includes PII or PHI for sentry, that the pre-send filter will catch
@test_pages.route("/logging_sentry/PII")
@limiter.exempt  # this route is exempt from the default limits
def error_PII():
    division_by_zero = "My social security number is 123-45-6789" / 0
    return division_by_zero


# rate limit example of one per day
@test_pages.route("/slow")
@limiter.limit("1 per day")
def slow():
    return "slow return - one per day"


## Data route for TESTING purposes of log, user activity, and role based access control
@test_pages.route("/data", methods=["GET"])
@login_required
@log_user_activity
@rbac()
def data():
    return jsonify({"data": "This is protected data."})
