from models.models import User  # Adjust the import path as necessary

# User loader
def load_user(user_id):
    return User.query.get(int(user_id))
