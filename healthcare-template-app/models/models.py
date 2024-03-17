# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime, timedelta
import secrets
import base64
import os

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(80), unique=True, nullable=False) # unique username
    password = db.Column(db.String(100), nullable=False) # password
    password_changed_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    otp_secret = db.Column(db.String(16), nullable=True) # 2FA secret
    failed_login_attempts = db.Column(db.Integer, default=0, nullable=False)  # Track failed login attempts
    lockout_until = db.Column(db.DateTime, nullable=True)  # Track lockout timestamp
    last_login_at = db.Column(db.DateTime, nullable=True)  # Last login date
    current_login_at = db.Column(db.DateTime, nullable=True)  # Current login date
    last_login_ip = db.Column(db.String(100), nullable=True)  # Last login IP address
    current_login_ip = db.Column(db.String(100), nullable=True)  # Current login IP address
    login_count = db.Column(db.Integer, default=0, nullable=False)  # Total login count
    ## relationships - UserActivityLog
    activity_logs = db.relationship('UserActivityLog', backref='user', lazy=True, cascade="all, delete-orphan")
    ## relationships - APIToken
    api_tokens = db.relationship('APIToken', backref='user', lazy=True, cascade="all, delete-orphan")
    ## relationships - Permission
    permissions = db.relationship('Permission', backref='user', lazy=True, cascade="all, delete-orphan")
    ## initialize the optional 2FA secret
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.otp_secret is None:
            # Generate a random secret for each new user
            self.otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')

class UserActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(80), nullable=False) # Foreign Key to User
    endpoint = db.Column(db.String(255), nullable=False)
    method = db.Column(db.String(10), nullable=False)
    accessed_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def __init__(self, user_id, username, endpoint, method):
        self.user_id = user_id
        self.username = username
        self.endpoint = endpoint
        self.method = method


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(80), nullable=False)
    object = db.Column(db.String(80), nullable=False)
    action = db.Column(db.String(80), nullable=False)

class APIToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    last_updated = db.Column(db.DateTime, default=datetime.now)

    def is_token_expired(self):
        return datetime.now() - self.last_updated > timedelta(days=7)

    @staticmethod
    def regenerate_token():
        return secrets.token_urlsafe()

    def update_token(self):
        self.token = self.regenerate_token()
        self.last_updated = datetime.now()

    ## create a function that we can call to generate a new row in the APIToken table
    @staticmethod
    def create_token(user_id, username):
        token = APIToken(user_id=user_id, username=username, token=APIToken.regenerate_token())
        db.session.add(token)
        db.session.commit()
        return token.token

