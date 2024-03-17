from app import app  # Import the Flask application instance
from models.models import db, Permission, User  # Import db, Permission, and User models

# Permissions to add
permissions_to_add = [
    ("alice", "/data", "GET"),
    ("janet", "/data", "GET"),
    ("john", "/data", "GET"),
    {"hants", "/data", "GET"},
    {"hants", "/profile", "GET"},
    {"hants", "/manage-permissions", "GET"},
    {"hants", "/manage-permissions", "POST"},
    {"hants", "/manage-permissions", "PUT"},
    {"hants", "/manage-permissions", "DELETE"},
]

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

        # Add users
        for user_info in users_to_add:
            if not User.query.filter_by(username=user_info["username"]).first():  # Check if user already exists
                new_user = User(username=user_info["username"], password=user_info["password"])
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
