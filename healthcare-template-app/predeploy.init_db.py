from app import app  # Import the Flask application instance
from models.models import (
    db,
    Permission,
    User,
    APIToken,
)  # Import db, Permission, and User models

from werkzeug.security import generate_password_hash
import secrets  # For generating secure tokens

def generate_secure_token():
    return secrets.token_urlsafe()  # Generates a URL-safe text string

# Permissions to add
permissions_to_add = [
    ("admin", "/manage-permissions/", "GET"),
    ("admin", "/manage-permissions/", "POST"),
    ("admin", "/manage-permissions/", "PUT"),
    ("admin", "/manage-permissions/", "DELETE"),
    ("admin", "/api/permissions/", "GET"),
    ("admin", "/api/permissions/", "POST"),
    ("admin", "/api/permissions/", "PUT"),
    ("admin", "/api/permissions/", "DELETE"),
    ("alice", "/manage-permissions/", "GET"),
    ("alice", "/manage-permissions/", "POST"),
    ("alice", "/manage-permissions/", "PUT"),
    ("alice", "/manage-permissions/", "DELETE"),
    ("alice", "/api/permissions/", "GET"),
    ("alice", "/api/permissions/", "POST"),
    ("alice", "/api/permissions/", "PUT"),
    ("alice", "/api/permissions/", "DELETE"),
]

# Users to add
users_to_add = [
    {"username": "admin", "password": "admin"},
    {"username": "alice", "password": "alice"},
]

def add_data():
    with app.app_context():
        db.create_all()  # Ensure all tables are created

        # Add users with hashed passwords
        for user_info in users_to_add:
            username = user_info["username"]
            password = user_info["password"]
            if not User.query.filter_by(
                username=username
            ).first():  # Check if user already exists
                hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
                print("Length of hashed password:", len(hashed_password))
                print("Hashed password: ", hashed_password)
                new_user = User(username=username, password=hashed_password)
                db.session.add(new_user)
                db.session.commit()

                # Retrieve the user to get the user ID
                new_user = User.query.filter_by(username=username).first()

                # Generate and add token for the new user
                token = generate_secure_token()
                new_token = APIToken(
                    user_id=new_user.id, username=username, token=token
                )
                db.session.add(new_token)
                db.session.commit()
                print(f"Added user {username} with token {token}")

        # Get a list of all usernames with their ids
        users = User.query.all()
        user_ids = {user.username: user.id for user in users}
        print(f"Users: {user_ids}")

        # Add permissions
        for subject, obj, action in permissions_to_add:
            if not Permission.query.filter_by(
                subject=subject, object=obj, action=action
            ).first():  # Check if permission already exists
                subject_id = user_ids[subject]
                print(
                    f"Adding permission for userid {subject_id} for {subject} on {obj} with action {action}"
                )
                new_permission = Permission(
                    user_id=subject_id, subject=subject, object=obj, action=action
                )
                db.session.add(new_permission)
                db.session.commit()

        print("Database initialized with users and permissions!")


if __name__ == "__main__":
    add_data()
