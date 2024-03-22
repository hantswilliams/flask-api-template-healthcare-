import requests

# Testing token endpoint: /api-token-test
# requires a header of X-API-Token with the token value
token = 'DMhdrh32NEWZELmei9oXlEgp1u10ErJdDr6kVLK6Hv8'
token_response = requests.get('http://localhost:5005/api/data/test', headers={'X-API-Token': token})
print(token_response.text)










##### Old version with session 

# Start a session
session = requests.Session()

# Log in
login_payload = {
    'username': 'hants',
    'password': 'hants'
}

login_response = session.post('http://127.0.0.1:5000/login', data=login_payload)
login_response.text

# Access protected endpoint
protected_response = session.get('http://127.0.0.1:5000/data')
print(protected_response.text)



# Add a new permission
new_permission = {
    'subject': 'cathy',
    'object': '/profile',
    'action': 'GET'
}

permission_response = session.post('http://127.0.0.1:5000/permissions', json=new_permission)
print(permission_response.text)

# Get list of permissions
permissions_response = session.get('http://127.0.0.1:5000/permissions')
print(permissions_response.text)








# Add a new permission for Dracula that does not exist as a user 
new_permission = {
    'subject': 'dracula',
    'object': '/profile',
    'action': 'GET'
}

permission_response = session.post('http://127.0.0.1:5000/permissions', json=new_permission)
print(permission_response.text)
### appears to still create, can perhaps handle this later
## logic would be if the user does not exist, you shouldnt be able to create a permission for them
