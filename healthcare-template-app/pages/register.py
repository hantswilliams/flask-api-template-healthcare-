from flask import Blueprint, render_template, request, redirect, url_for, current_app
from models.models import db, APIToken
import pyotp
import pyqrcode
from util.auth.auth import User, validate_password
from werkzeug.security import generate_password_hash, check_password_hash

# Create a Blueprint
register_pages = Blueprint("register_pages", __name__)


# Example route within your blueprint
## Register route
@register_pages.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Validate the password
        valid, message = validate_password(password)
        if not valid:
            return render_template(
                "registration.html", message=message, username=username
            )

        # Continue with user creation if the password is valid
        # Remember to hash the password before storing it
        user = User(username=username, password=generate_password_hash(password, method="pbkdf2:sha256"))
        db.session.add(user)
        db.session.commit()

        # Create a new token for the user
        user = User.query.filter_by(username=username).first()
        APIToken.create_token(user.id, user.username)

        return redirect(url_for("register_pages.twofa", user_id=user.id))

    return render_template("registration.html")


@register_pages.route("/twofa/<int:user_id>")
def twofa(user_id):
    user = User.query.get(user_id)
    if user is None:
        return "User not found", 404
    otpauth_url = pyotp.totp.TOTP(user.otp_secret).provisioning_uri(
        user.username, issuer_name="Flask Healthcare Template"
    )
    qr_code = pyqrcode.create(otpauth_url)
    qr_code.png("static/user_{}.png".format(user_id), scale=5)

    return render_template("twofa.html", user_id=user_id)


## 2FA setup route for admin or existing user, reset 2FA
@register_pages.route("/admin/2fa/setup", methods=["GET", "POST"])
def admin_2fa_setup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # Validate the username and password
        user = User.query.filter_by(username=username).first()
        if user is None:
            return "User not found", 404
        # Verify the password
        if user and check_password_hash(user.password, password):
            otpauth_url = pyotp.totp.TOTP(user.otp_secret).provisioning_uri(
                user.username, issuer_name="Flask Healthcare Template"
            )
            qr_code = pyqrcode.create(otpauth_url)
            qr_code.png("static/user_{}.png".format(user.id), scale=5)
            return render_template("twofa.html", user_id=user.id)

    return render_template("twofa_admin.html")
