"""
Test script to verify the hate speech detection system
"""

import requests
import json

API_URL = "http://localhost:5000/api"

def test_api_connection():
    """Test API connection"""
    print("\n" + "="*50)
    print("Testing API Connection")
    print("="*50)
    
    try:
        response = requests.get("http://localhost:5000/")
        if response.status_code == 200:
            print("✅ API is online and responding")
            print(json.dumps(response.json(), indent=2))
            return True
        else:
            print("❌ API returned error status")
            return False
    except Exception as e:
        print(f"❌ Could not connect to API: {e}")
        print("Make sure the backend is running: python backend/app.py")
        return False

def test_text_analysis():
    """Test text analysis endpoint"""
    print("\n" + "="*50)
    print("Testing Text Analysis")
    print("="*50)
    
    test_cases = [
        {
            "text": "Have a wonderful day! You're amazing!",
            "user_id": 1,
            "username": "test_user1",
            "expected": "normal"
        },
        {
            "text": "You are stupid and worthless, I hate you",
            "user_id": 2,
            "username": "test_user2",
            "expected": "hate_speech"
        },
        {
            "text": "Let's work together on this project",
            "user_id": 3,
            "username": "test_user3",
            "expected": "normal"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}:")
        print(f"Text: {test_case['text']}")
        print(f"Expected: {test_case['expected']}")
        
        try:
            response = requests.post(
                f"{API_URL}/analyze",
                json={
                    "text": test_case['text'],
                    "user_id": test_case['user_id'],
                    "username": test_case['username']
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                is_hate = result['result']['is_hate_speech']
                confidence = result['result']['confidence']
                
                print(f"Result: {'Hate Speech' if is_hate else 'Normal'}")
                print(f"Confidence: {confidence:.3f}")
                print(f"Action: {result['action_taken']}")
                
                if is_hate and test_case['expected'] == 'hate_speech':
                    print("✅ PASS")
                elif not is_hate and test_case['expected'] == 'normal':
                    print("✅ PASS")
                else:
                    print("⚠️ UNEXPECTED RESULT")
            else:
                print(f"❌ Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")

def test_statistics():
    """Test statistics endpoint"""
    print("\n" + "="*50)
    print("Testing Statistics Endpoint")
    print("="*50)
    
    try:
        response = requests.get(f"{API_URL}/statistics")
        if response.status_code == 200:
            stats = response.json()['statistics']
            print("\n📊 Platform Statistics:")
            print(f"  Total Users: {stats['total_users']}")
            print(f"  Active Users: {stats['active_users']}")
            print(f"  Suspended Users: {stats['suspended_users']}")
            print(f"  Total Violations: {stats['total_violations']}")
            print(f"  Total Posts: {stats['total_posts']}")
            print(f"  Hate Speech Rate: {stats['hate_speech_percentage']}%")
            print("✅ Statistics retrieved successfully")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_user_management():
    """Test user management endpoints"""
    print("\n" + "="*50)
    print("Testing User Management")
    print("="*50)
    
    try:
        response = requests.get(f"{API_URL}/users")
        if response.status_code == 200:
            users = response.json()['users']
            print(f"\n✅ Found {len(users)} users")
            
            if len(users) > 0:
                print(f"\nSample user:")
                print(json.dumps(users[0], indent=2))
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("HATE SPEECH DETECTION SYSTEM - TEST SUITE")
    print("="*60)
    
    # Test API connection
    if not test_api_connection():
        print("\n❌ Cannot proceed with tests. Backend API is not running.")
        print("Please start the backend: python backend/app.py")
        return
    
    # Run tests
    test_text_analysis()
    test_statistics()
    test_user_management()
    
    print("\n" + "="*60)
    print("✅ Test Suite Completed")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
