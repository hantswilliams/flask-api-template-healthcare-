# HIPAA / HITRUST items covered in this example app:

A brief demo of potential HIPAA / HITRUST items that can be covered in a Flask application.
This is for demonstration pursposes and learning, showcasing the flexibility of Flask. The template for this flask ask can be found in the `/healthcare-template-app` directory.

## Notes to self: 
- Pages: 
    - This folder contains web pages that are rendered by the Flask app.
    - Right now these are basic, and if you want to display json here, use JSONIFY from flask
    - These use the Jinja2 templating engine, along with HTML, CSS, and JS
    - Managed by FLASK BLUEPRINTS
    - Decorators go within the route itself, versus in the class method like in the API
- API:
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

```
REDIS_ENDPOINT = 
SENTRY_DSN = 
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


