# Structure of the Healthcare Template App

## Pages Folder: 
    - Inspired by Next.js, which has a `pages` folder that contains relevant server/client side code for the html template pages 
    - This folder contains the Flask Blueprints that are used to render the web pages
    - These use the Jinja2 templating engine, along with HTML, CSS, and JS
    - Decorators go within the route itself, versus in the class method like in the API

## Templates Folder: 
- Just like a standard Flask app, this folder contains the HTML templates that are rendered by the Flask Blueprints
- Based on the Talisman settings found in `util/config/loader.py` file, we are enabling scripts to be executed that exist in the .html page, but not from external sources. So in order for the `<script>` tags to work properly, need to have the it look like: `<script nonce="{{ csp_nonce() }}">` in the .html pages that contain a script tag.
- So when you create new .html files with script tags within the templates folder, make sure to include the `nonce="{{ csp_nonce() }}"` within the script tag. 

## API Folder
    - Also inspired by Next.js, with the idea of having a `api` folder that contains all of the relevant code for API endpoints
    - These are managed by FLASK_RESTX 
    - Each of these endpoints automatically generates a Swagger UI page
    - Each of these endpoints will automatically convert to JSON, no need for jsonify
    - Each of these require a namespace, and a class that inherits from Resource
        - The class will have methods for each method (GET, POST, PUT, DELETE)
        - Each method will have a decorator that specifies the route, and the expected parameters
        - Inside of the class method, we then put the decorators like @token_required, @rbac(), and  @limiter.limit("1 per sec"); versus in the route itself like in the pages





