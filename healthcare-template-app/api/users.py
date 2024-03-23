from flask import request, redirect, url_for
from flask_login import login_required
from flask_restx import Namespace, Resource
from models.models import User, db, APIToken
from werkzeug.security import generate_password_hash

api = Namespace('users', description='internal users, not for public use')

@api.route('/')
class Subjects(Resource):
    @login_required
    def get(self):
        subjects = [user.username for user in User.query.all()]
        return subjects, 200

## TO UPDATE: add users, should also move to a namespace in the api folder
@api.route('/add', methods=['POST'])
class AddUser(Resource):
    @login_required
    def post(self):

        # Extract user details from form data or JSON
        username = request.form.get('username')
        password = request.form.get('password')
        # Implement validation as needed
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return {'message': 'User already exists'}, 400

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Now create a new token for the user
        new_user = User.query.filter_by(username=username).first()
        ## then create the token
        APIToken.create_token(new_user.id, new_user.username)
        return redirect(url_for('permission_pages.permissions_view'))

## TO UPDATE: edit users, should also move to a namespace in the api folder
@api.route('/edit-user/<int:user_id>', methods=['POST'])
class EditUser(Resource):
    @login_required
    def post(self, user_id):
        user = User.query.get_or_404(user_id)
        # For simplicity, only updating password here
        new_password = request.form.get('new_password')
        user.password = generate_password_hash(new_password)
        db.session.commit()
        return redirect(url_for('permission_pages.permissions_view'))

# ## TO UPDATE: delete users, should also move to a namespace in the api folder
@api.route('/delete-user/<int:user_id>', methods=['POST'])
class DeleteUser(Resource):
    @login_required
    def post(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('permission_pages.permissions_view'))



