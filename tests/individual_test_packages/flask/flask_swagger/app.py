from flask import Flask, request
from flask_restx import Api, Resource, fields

app = Flask(__name__)

api = Api(
    app, doc='/swagger', 
    version='1.0', title='Sample API',
    description='A sample API')

@app.route('/redoc')
def redoc():
    return '''
    <!DOCTYPE html>
    <html>
      <head>
        <title>ReDoc</title>
        <!-- Redoc's latest version CDN -->
        <script src="https://cdn.jsdelivr.net/npm/redoc/bundles/redoc.standalone.js"></script>
      </head>
      <body>
        <redoc spec-url='/swagger.json'></redoc>
        <script nonce="{{ csp_nonce() }}">
          Redoc.init('/swagger.json')
        </script>
      </body>
    </html>
    '''

ns_hello = api.namespace('hello', description='Hello operations')
ns_goodbye = api.namespace('goodbye', description='Goodbye operations')
ns_math = api.namespace('math', description='Math operations')



##################################################################
@ns_hello.route('/')
class HelloWorld(Resource):
    def get(self):
        """Returns 'Hello, World!'"""
        return {'hello': 'world'}
##################################################################


##################################################################    
@ns_goodbye.route('/')
class GoodbyeWorld(Resource):
    def get(self):
        """Returns 'Goodbye, World!'"""
        return {'goodbye': 'world'}
################################################################## 


##################################################################
# Define the expected input model for your endpoint
input_model = api.model('Math Multiply Input Model', {
    'number': fields.Integer(required=True, description='A number to multiply')
})

# Define the output model for documentation
output_model = api.model('Math Multiply Output Model', {
    'result': fields.Integer(description='Result of multiplication')
})
@ns_math.route('/multiply')
class Multiply(Resource):
    @ns_math.doc('multiply_number')
    @ns_math.expect(input_model, validate=True)
    @ns_math.marshal_with(output_model)
    def post(self):
        """Multiply a number by 10"""
        data = request.json
        number = data.get('number')
        result = number * 10
        return {'result': result}
##################################################################






if __name__ == '__main__':
    app.run(debug=True)
