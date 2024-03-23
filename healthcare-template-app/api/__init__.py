from flask_restx import Api
from api.data import api as data
from api.permissions import api as permissions
from api.users import api as users

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-API-Token'
    }
}

api = Api(
    title='Flask Healthcare App Template',
    prefix="/api",
    doc='/swagger', 
    version='1.0', 
    description='A template for a Flask app that provides a RESTful API for healthcare data',
    authorizations=authorizations,
    security='apikey'  # Apply the apiKey security to all endpoints
)

api.add_namespace(data)
api.add_namespace(permissions)
api.add_namespace(users)