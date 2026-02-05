import requests
import time

# Wait a moment for server to be fully ready
time.sleep(2)

# Test registration endpoint
try:
    response = requests.post(
        'http://localhost:5000/api/auth/register',
        json={
            'username': 'testuser1',
            'email': 'test1@example.com',
            'password': 'pass123'
        }
    )
    print(f'Status Code: {response.status_code}')
    print(f'Response: {response.json()}')
except Exception as e:
    print(f'Error: {e}')
