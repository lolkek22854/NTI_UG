import requests
print(requests.post('http://127.0.0.1:5000/send_data', data={'id': 133, 'points': 40}).content)
print(requests.post('http://127.0.0.1:5000/check_id', data={'id': 123}))