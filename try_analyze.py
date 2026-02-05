import requests

payload = {
    'text': 'you are useless is hate but it is posting',
    'user_id': 1532686,
    'username': 'testuser1'
}

r = requests.post('http://localhost:5000/api/analyze', json=payload)
print('Status:', r.status_code)
print('Response:', r.json())
