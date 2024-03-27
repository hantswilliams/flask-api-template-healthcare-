from flask import Blueprint, render_template, current_app as app
from flask_login import login_required
from models.models import Permission, User
from util.auth.auth import log_user_activity
from util.rbac.rbac import rbac

# Create a Blueprint
permission_pages = Blueprint("permission_pages", __name__)


## ADMIN route for managing RBAC permissions, creating new users, deleting users, resetting passwords
@permission_pages.route("/")
@login_required
@log_user_activity
@rbac()
def permissions_view():
    permissions = Permission.query.all()
    users = User.query.all()
    routes = []
    for i in app.url_map.iter_rules():
        if i.endpoint != "static":  # Skip the static endpoint provided by Flask
            endpoint_value = str(i).replace("<", "{").replace(">", "}")
            endpoint_value = endpoint_value.split("{")[0]
            routes.append(
                {
                    "endpoint": endpoint_value,
                    "methods": list(i.methods - set(["HEAD", "OPTIONS"])),
                }
            )

    return render_template(
        "permissions.html", permissions=permissions, users=users, routes=routes
    )
