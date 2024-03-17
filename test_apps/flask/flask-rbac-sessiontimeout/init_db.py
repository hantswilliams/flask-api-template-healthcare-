from app import app  # Import the Flask application instance
from models.models import db, Permission, User  # Import db, Permission, and User models
from werkzeug.security import generate_password_hash

# Permissions to add
permissions_to_add = [
    ("alice", "/data", "GET"),
    ("alice", "/manage-permissions", "GET"),
    ("alice", "/manage-permissions", "POST"),
    ("alice", "/manage-permissions", "PUT"),
    ("alice", "/manage-permissions", "DELETE"),
    ("janet", "/data", "GET"),
    ("john", "/data", "GET")]

# Users to add
users_to_add = [
    {"username": "alice", "password": "alice"},
    {"username": "bob", "password": "bob"},
    {"username": "cathy", "password": "cathy"},
    {"username": "hants", "password": "hants"},
    {"username": "john", "password": "john"}
]

def add_data():
    with app.app_context():
        db.create_all()  # Ensure all tables are created

        # Add users with hashed passwords
        for user_info in users_to_add:
            username = user_info["username"]
            password = user_info["password"]
            if not User.query.filter_by(username=username).first():  # Check if user already exists
                hashed_password = generate_password_hash(password)  # Hash the password
                new_user = User(username=username, password=hashed_password)
                db.session.add(new_user)

        # Add permissions
        for subject, obj, action in permissions_to_add:
            if not Permission.query.filter_by(subject=subject, object=obj, action=action).first():  # Check if permission already exists
                new_permission = Permission(subject=subject, object=obj, action=action)
                db.session.add(new_permission)

        db.session.commit()
        print("Database initialized with users and permissions!")

if __name__ == '__main__':
    add_data()
