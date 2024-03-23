from flask_restx import Namespace, Resource
from util.auth.tokens import token_required
from util.rbac.rbac import rbac
from util.rate_limiting.rate_limiter import limiter

api = Namespace(
    'data', 
    description="""This is a simple EXTERNAL FACING example of a data API endpoint that requires a token and RBAC permissions for your user token. In the soure code, you can see that this has the @token_required, @rbac(), and @limiter.limit to control access to this endpoint. This is a simple test endpoint to check. Recommend that you use this as a template for your own data API endpoints. """,
)

### Simple test endpoint to check if the API is working with TOKEN and RBAC
@api.route('/test')
class DataTest(Resource):
    @token_required
    @rbac()
    @limiter.limit("1 per sec")
    def get(self):
        return {'message': 'You are authorized to access this endpoint!'}, 200

