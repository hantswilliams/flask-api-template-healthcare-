from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.models import APIToken
from util.auth.auth import log_user_activity 
from util.data_access.permissions import get_user_permissions

# Create a Blueprint
profile_pages = Blueprint('profile_pages', __name__)

## Profile route
@profile_pages.route('/')
@login_required
@log_user_activity
def profile():
    ## get permissions
    user_permissions = get_user_permissions(current_user.id)
    ## get user token
    user_token = APIToken.query.filter_by(username=current_user.username).first()
    if user_token:
        user_token = user_token.token
    else:
        user_token = "No token found"
    return render_template('profile.html',
                           username=current_user.username,
                           userid=current_user.id,
                           user_permissions=user_permissions,
                           user_token=user_token)