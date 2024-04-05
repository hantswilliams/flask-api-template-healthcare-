from datetime import datetime, timedelta
from flask import (
    Blueprint,
    request,
    render_template,
    jsonify,
    redirect,
    url_for,
    current_app,
)
from flask_login import login_user, current_user
from models.models import db, User
import pyotp
from util.auth.auth_audit import update_login_audit_info
from util.rate_limiting.rate_limiter import limiter
from werkzeug.security import check_password_hash

login_pages = Blueprint("login_pages", __name__)


@login_pages.route("/", methods=["GET", "POST"])
@limiter.limit("5 per minute")
# @limiter.exempt ## for testing purposes
def login():
    ## determine if 2FA is required, get lockout duration, get password age
    twoFactor = current_app.config.get("TWO_FACTOR_AUTH_REQUIRED", True)
    account_lockout_time = current_app.config.get("ACCOUNT_LOCKOUT_TIME_MINS", 15)
    password_age_days = current_app.config.get("PASSWORD_AGE_RESET_DAYS", 90)


    if current_user.is_authenticated:
        return redirect(
            url_for("profile_pages.profile"), 302
        )  # Redirect to the profile page if already logged in

    if request.method == "GET":
        return render_template(
            "login.html", twoFactor=twoFactor
        )  # Render the login page on GET requests

    # Handling POST request via AJAX
    data = request.json
    username = data.get("username")
    password = data.get("password")
    token = data.get("token")

    user = User.query.filter_by(username=username).first()

    if user and user.lockout_until and user.lockout_until > datetime.now():
        return jsonify(
            {
                "success": False,
                "message": "Account locked. Please try again in " + str(account_lockout_time) + " minutes",
                "remaining_attempts": 0,
            }
        )

    remaining_attempts = max(0, 5 - user.failed_login_attempts) if user else 5

    if user and check_password_hash(user.password, password):
        password_age = datetime.now() - user.password_changed_at

        if password_age > timedelta(days=password_age_days):
            login_user(user)
            return jsonify({
                "success": True, 
                "redirect": url_for("change_password")
                })

        elif password_age < timedelta(days=password_age_days) and not twoFactor:
            update_login_audit_info(user, request.remote_addr)
            user.failed_login_attempts = 0
            db.session.commit()
            login_user(user)
            return jsonify(
                {
                    "success": True, 
                    "redirect": url_for("profile_pages.profile")
                }
            )

        elif twoFactor and pyotp.TOTP(user.otp_secret).verify(token):
            update_login_audit_info(user, request.remote_addr)
            user.failed_login_attempts = 0
            db.session.commit()
            login_user(user)
            return jsonify(
                {
                    "success": True, 
                    "redirect":  url_for("profile_pages.profile")
                }
            )

        else:
            return jsonify(
                {
                    "success": False,
                    "message": "Invalid 2FA token",
                    "remaining_attempts": remaining_attempts,
                }
            )

    else:
        if user:
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= 5:
                user.lockout_until = datetime.now() + timedelta(minutes=account_lockout_time)
            db.session.commit()
            remaining_attempts = max(0, 5 - user.failed_login_attempts)
        return jsonify(
            {
                "success": False,
                "message": "Invalid username or password",
                "remaining_attempts": remaining_attempts,
            }
        )
