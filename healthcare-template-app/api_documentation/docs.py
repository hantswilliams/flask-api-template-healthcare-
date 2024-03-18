from flask_restx import Api

def flask_api_docs(app):
    api = Api(
        app, 
        prefix="/api",
        doc='/swagger', 
        version='1.0', title='Flask Healthcare App Template',
        description='A template for a Flask app that provides a RESTful API for healthcare data',
    )
    return api
