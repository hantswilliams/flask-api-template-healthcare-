from flask_restx import Api
from api.ns_data import api as data_ns

api = Api(
    title='Flask Healthcare App Template',
    prefix="/api",
    doc='/swagger', 
    version='1.0', 
    description='A template for a Flask app that provides a RESTful API for healthcare data',
)

api.add_namespace(data_ns)