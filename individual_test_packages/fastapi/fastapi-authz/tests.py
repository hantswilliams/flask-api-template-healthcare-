import requests 

## curl -i http://127.0.0.1:8000/dataset1/protected

response = requests.get('http://127.0.0.1:8000/dataset1/protected', auth=('hants', 'password'))
print(response.text)
