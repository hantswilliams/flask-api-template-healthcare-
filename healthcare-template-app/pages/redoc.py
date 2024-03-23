from flask import Blueprint

# Create a Blueprint
redoc_pages = Blueprint('redoc_pages', __name__)

## Redoc route
@redoc_pages.route('/')
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
        <redoc spec-url='/api/swagger.json'></redoc>
        <script>
          Redoc.init('/api/swagger.json')
        </script>
      </body>
    </html>
    '''
