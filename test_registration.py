"""
Test registration endpoint
"""
import requests
import json

url = 'http://localhost:5000/api/auth/register'
data = {
    'username': 'testuser123',
    'email': 'test123@test.com',
    'password': 'password123'
}

try:
    print(f"🔄 Testing registration at {url}")
    print(f"📤 Data: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, json=data)
    
    print(f"\n📊 Status Code: {response.status_code}")
    print(f"📥 Response: {response.text}")
    
    if response.status_code == 201:
        print("\n✅ Registration successful!")
    else:
        print(f"\n❌ Registration failed: {response.status_code}")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
