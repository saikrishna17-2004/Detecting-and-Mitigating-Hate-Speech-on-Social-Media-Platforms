import requests

# Test login endpoint with the user we just created
try:
    response = requests.post(
        'http://localhost:5000/api/auth/login',
        json={
            'username': 'testuser1',
            'password': 'pass123'
        }
    )
    print(f'Status Code: {response.status_code}')
    print(f'Response: {response.json()}')
except Exception as e:
    print(f'Error: {e}')
