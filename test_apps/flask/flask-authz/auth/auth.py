from flask_login import UserMixin

# Dummy user storage for demonstration
users = {
    'alice': {'password': 'password1'},
    'bob': {'password': 'password2'},
    'cathy': {'password': 'password3'},
    'hants': {'password': 'hants'}
}

# User class
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# User loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None
