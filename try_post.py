import requests

payload = {
    'content': 'you are useless is hate but it is posting',
    'user_id': 1532686,
    'image_url': None
}

r = requests.post('http://localhost:5000/api/posts', json=payload)
print('Status:', r.status_code)
try:
    print('Response:', r.json())
except Exception as e:
    print('Non-JSON response:', r.text)
