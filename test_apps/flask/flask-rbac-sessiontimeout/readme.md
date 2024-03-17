# HIPAA / HITRUST items covered in this example app:

1. RBAC - prevents unauthorized access to PHI
    - With simple dedicated GUI for admin to manage roles-permissions, and users 
2. Session Timeout - prevents unauthorized access to PHI
    - Currently set to 5 minutes
3. Session Security:
    - Session cookie is only allowed over HTTPS (SESSION_COOKIE_SECURE)
    - Session cookie is only allowed to be accessed by the server (SESSION_COOKIE_HTTPONLY)
    - Session cookie is only allowd by the server that set it (SESSION_COOKIE_SAMESITE)
3. Minimum password length and complexity - prevents weak passwords
    - Currently set to 8 characters, 1 uppercase, 1 lowercase, 1 number, 1 special character
4. Account lockout - prevents brute force attacks
    - Currently set to 5 attempts, lockout for 15 minutes
5. Login audit trail - tracks who is accessing PHI
    - Captures IP address, username, and timestamp
6. User activity audit trail - tracks what users are doing with PHI
    - Captures all endpoints accessed, method, and timestamp
7. Password expiration - prevents unauthorized access to PHI 
    - Currently set to 90 days
8. Overall application monitoring - 
    - Currently with Sentry.io
    - Have built in basic RegEx rules to reduce/prevent PHI (or PII) from being logged in Sentry
9. Rotating API tokens - prevents unauthorized access to PHI
    - Currently set to 7 days
    - The config is found in the DB model: `APIToken`


## Decesions 
- API is stateless; requires token that is rotated every 7 days, and associated with a users role and permissions 
    - form of mainintaing least based access/privileges for handling PHI/PII 


