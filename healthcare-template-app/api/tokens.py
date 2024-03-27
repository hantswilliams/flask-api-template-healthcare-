from flask_login import current_user
from flask_restx import Namespace, Resource
from models.models import APIToken
from util.auth.tokens import token_required

api = Namespace("token", description="API tokens for users available via API")


@api.route("/")
class Subjects(Resource):
    @token_required
    def get(self):
        user_token = APIToken.query.filter_by(username=current_user.username).first()
        if user_token:
            return {"token": user_token.token, "last_updated": user_token.last_updated}
        return {"message": "No API token found. Please generate one."}


# generate API token route
@api.route("/generate", methods=["GET"])
class AddUser(Resource):
    @token_required
    def get(self):
        user_token = APIToken.query.filter_by(user_id=current_user.id).first()

        if user_token:
            user_token.update_token()
            user_token = APIToken.query.filter_by(user_id=current_user.id).first()
            return {"token": user_token.token, "last_updated": user_token.last_updated}

        else:
            APIToken.create_token(current_user.id, current_user.username)
            user_token = APIToken.query.filter_by(user_id=current_user.id).first()
            return {"token": user_token.token, "last_updated": user_token.last_updated}
