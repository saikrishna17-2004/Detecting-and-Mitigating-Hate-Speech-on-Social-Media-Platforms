import requests

# Test health
try:
    r = requests.post('http://localhost:5000/api/analyze', json={'text': 'hello world', 'user_id': 1})
    print('Analyze Status:', r.status_code)
    print('Analyze Response:', r.json())
except Exception as e:
    print('Analyze Error:', e)

# Test registration
try:
    r = requests.post('http://localhost:5000/api/auth/register', json={'username': 'testuser2', 'email': 'test2@example.com', 'password': 'pass123'})
    print('\nRegister Status:', r.status_code)
    print('Register Response:', r.json())
except Exception as e:
    print('\nRegister Error:', e)
