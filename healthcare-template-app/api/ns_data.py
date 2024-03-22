from flask_restx import Namespace, Resource
from util.auth.tokens import token_required
from util.rbac.rbac import rbac
from util.rate_limiting.rate_limiter import limiter

api = Namespace('data', description='data operations')

@api.route('/test')
class DataTest(Resource):
    @token_required
    @rbac()
    @limiter.limit("1 per sec")
    def get(self):
        return {'message': 'You are authorized to access this endpoint!'}, 200
