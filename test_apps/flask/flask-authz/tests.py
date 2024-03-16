import requests

# Start a session
session = requests.Session()

# Log in
login_payload = {
    'username': 'alice',
    'password': 'password1'
}

login_response = session.post('http://127.0.0.1:5000/login', data=login_payload)

# Access protected endpoint
protected_response = session.get('http://127.0.0.1:5000/data')
print(protected_response.text)
