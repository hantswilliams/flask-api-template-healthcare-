import requests

url = 'http://127.0.0.1:5000/math/multiply'

data = {
    'number': 5
}

# Make sure to specify that you're sending JSON data
response = requests.post(url, json=data)

# Print the response to see the result
print(response.text)
