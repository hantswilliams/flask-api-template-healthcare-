from flask import Blueprint, redirect, jsonify
from flask_login import login_required, current_user
from models.models import db, APIToken

# Create a Blueprint
token_pages = Blueprint('token_pages', __name__)

## Retrieve logged in user API token route
@token_pages.route('/')
@login_required
def my_api_token():
    user_token = APIToken.query.filter_by(username=current_user.username).first()
    if user_token:
        return jsonify({'token': user_token.token, 'last_updated': user_token.last_updated})
    return jsonify({'message': 'No API token found. Please generate one.'})

## Generate API token route
@token_pages.route('/generate', methods=['GET'])
@login_required
def generate_api_token():
    user_token = APIToken.query.filter_by(user_id=current_user.id).first()
    
    if user_token:
        user_token.update_token()
    else:
        APIToken.create_token(current_user.id, current_user.username)

    db.session.commit()
    return redirect('/api-token')