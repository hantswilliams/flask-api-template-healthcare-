from pages.session_time import session_time
from pages.permissions import permission_pages
from pages.login import login_pages
from pages.logout import logout_pages
from pages.landing import landing_pages
from pages.profile import profile_pages
from pages.register import register_pages
from pages.changePassword import changepassword_pages
from pages.apiTokens import token_pages
from pages.redoc import redoc_pages
from pages.tests import test_pages

# Add all the Blueprints to a list (or a dictionary, if you prefer)
blueprints = [
    (landing_pages, "/"),
    (token_pages, "/api-token"),
    (changepassword_pages, "/change_password"),
    (login_pages, "/login"),
    (logout_pages, "/logout"),
    (permission_pages, "/manage-permissions"),
    (profile_pages, "/profile"),
    (redoc_pages, "/redoc"),
    (register_pages, "/register"),
    (session_time, "/session-time"),
    (test_pages, "/test"),
]


def register_blueprints(app):
    for blueprint, url_prefix in blueprints:
        app.register_blueprint(blueprint, url_prefix=url_prefix)
