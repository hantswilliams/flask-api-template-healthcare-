# HIPAA / HITRUST items covered in this example app:

A brief demo of potential HIPAA / HITRUST items that can be covered in a Flask application.
This is for demonstration pursposes and learning, showcasing the flexibility of Flask. The template for this flask ask can be found in the `/healthcare-template-app` directory.

## Notes to self: 
- Pages: 
    - inspired by Next.js, and the idea of having a `pages` folder
    - This folder contains web pages that are rendered by the Flask app.
    - Right now these are basic, and if you want to display json here, use JSONIFY from flask
    - These use the Jinja2 templating engine, along with HTML, CSS, and JS
    - Managed by FLASK BLUEPRINTS
    - Decorators go within the route itself, versus in the class method like in the API
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
- The PRODUCTION_ENV is used to determine if the app is in production or not. The options are True or False. If you select FALSE, it will use the `configDev.yaml` file. If you select TRUE, it will use the `configProd.yaml` file.
- The REDIS_ENDPOINT is a dependency for the rate limiter. Recommend using the free tier of RedisLabs.
- The SENTRY_DSN is used for error logging. It is required. It is free for up to 5000 (?)events per month.
- The SECRET_KEY is used for the Flask app. It is required.
- The SQLALCHEMY_DATABASE_URI is used for the database connection. It is required. Currently have only tested with SQLite. Plan on updating with MySQL and PostgreSQL.

```
PRODUCTION_ENV = 
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


## HIPAA / HITRUST items covered in this example app:

1. RBAC - prevents unauthorized access to PHI
    - With simple dedicated GUI for admin to manage roles-permissions, and users 
2. 2-Factor Authentication - prevents unauthorized access to PHI
    - Currently set to Google Authenticators
3. Session Timeout - prevents unauthorized access to PHI
    - Currently set to 5 minutes
4. Session Security:
    - Session cookie is only allowed over HTTPS (SESSION_COOKIE_SECURE)
    - Session cookie is only allowed to be accessed by the server (SESSION_COOKIE_HTTPONLY)
    - Session cookie is only allowd by the server that set it (SESSION_COOKIE_SAMESITE)
5. Minimum password length and complexity - prevents weak passwords
    - Currently set to 8 characters, 1 uppercase, 1 lowercase, 1 number, 1 special character
6. Account lockout - prevents brute force attacks
    - Currently set to 5 attempts, lockout for `15 minutes`
7. Login audit trail - tracks who is accessing PHI
    - Captures IP address, username, and timestamp
    - Currently part of `User` model table
8. User activity audit trail - tracks what users are doing with PHI
    - Captures all endpoints accessed, method, and timestamp
    - Currently in datatable called `UserActivityLog`
9. Password expiration - prevents unauthorized access to PHI 
    - Currently set to 90 days
10. Overall application monitoring - 
    - Currently with Sentry.io
    - Have built in basic RegEx rules to reduce/prevent PHI (or PII) from being logged in Sentry
11. Rotating API tokens - prevents unauthorized access to PHI
    - Currently set to 7 days
    - The config is found in the DB model: `APIToken`
12. API limiting 
    - Each end up currently has a set limit of 1 request per second
    - Can individually set limits for each endpoint

## Decesions 
- API is stateless; requires token that is rotated every 7 days, and associated with a users role and permissions 
    - form of mainintaing least based access/privileges for handling PHI/PII 


