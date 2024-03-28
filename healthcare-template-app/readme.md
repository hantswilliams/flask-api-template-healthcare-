


## Notes to self: 
- Pages: 
    - inspired by Next.js, and the idea of having a `pages` folder
    - This folder contains web pages that are rendered by the Flask app.
    - Right now these are basic, and if you want to display json here, use JSONIFY from flask
    - These use the Jinja2 templating engine, along with HTML, CSS, and JS
    - Managed by FLASK BLUEPRINTS
    - Decorators go within the route itself, versus in the class method like in the API
- Security and Templates
    - Based on the Talisman settings flound in loader.py file, we are enabling scripts to be executed that exist in the .html page, but not from external sources. So in order for the `<script>` tags to work properly, need to have the it look like: `<script nonce="{{ csp_nonce() }}">` in the .html pages that contain a script tag.
- API:
    - inspired by Next.js, and the idea of having a `api` folder
    - This folder contains the API endpoints that are used by the front end
    - These are managed by FLASK_RESTX 
    - Each of these endpoints automatically generates a Swagger UI page
    - Each of these endpoints will automatically convert to JSON, no need for jsonify
    - Each of these require a namespace, and a class that inherits from Resource
        - The class will have methods for each HTTP method (GET, POST, PUT, DELETE)
        - Each method will have a decorator that specifies the route, and the expected parameters
        - Inside of the class method, we then put the decorators like @token_required, @rbac(), and  @limiter.limit("1 per sec"); versus in the route itself like in the pages

## ENV file Structure 

The `.env` file should be structured as follows, and found in the root directory of the project. 
- The ENVIRONMENT is used to determine if the app is in development, staging, or production. The options are DEV, STAGING, or PROD. As a example, if you select DEV, it will use the `configDev.yaml` file. 
- The REDIS_ENDPOINT is a dependency for the rate limiter. Recommend using the free tier of RedisLabs.
- The SENTRY_DSN is used for error logging. It is required. It is free for up to 5000 (?)events per month.
- The SECRET_KEY is used for the Flask app. It is required.
- The SQLALCHEMY_DATABASE_URI is used for the database connection. It is required. Currently have only tested with SQLite. Plan on updating with MySQL and PostgreSQL.

```
ENVIRONMENT = 
REDIS_ENDPOINT = 
SENTRY_DSN = 
SECRET_KEY = 
SQLALCHEMY_DATABASE_URI = 
```

## Configuration File (DEV) . YAML file 

The `configDEV.yaml` file should be structured as follows, and found in the root directory of the project. There is a DEV and a PROD (`configProd.yaml`) file. 

```
# Sessions/Cookies
PERMANENT_SESSION_LIFETIME: 15  # number in minutes; this is how long the session will last
SESSION_COOKIE_SECURE: False # should be set to True in production - makes requirement for HTTPS
SESSION_COOKIE_HTTPONLY: True # should be set to True in production; prevents JavaScript from accessing the cookie
SESSION_COOKIE_SAMESITE: Lax # or Strict, None - can use Strict if you are paranoid about CSRF attacks
REMEMBER_COOKIE_DURATION: 7 # number of DAYS to remember the user

# Password restrictions
PASSWORD_MIN_LENGTH: 8
PASSWORD_REQ_UPPERCASE: True
PASSWORD_REQ_LOWERCASE: True
PASSWORD_REQ_DIGIT: True
PASSWORD_REQ_SPECIAL: True

# API Tokens
TOKEN_EXPIRATION_DAYS: 7 # days untill the token will expire
```


## Decesions 
- API is stateless; requires token that is rotated every 7 days, and associated with a users role and permissions 
    - form of mainintaing least based access/privileges for handling PHI/PII 


