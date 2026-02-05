"""
Quick API Test Script
"""
import requests
import json
import time

print("\n" + "="*60)
print("🧪 TESTING BACKEND API")
print("="*60 + "\n")

# Wait for server to be ready
print("Waiting for server...")
time.sleep(2)

BASE_URL = "http://localhost:5000"

# Test 1: Root endpoint
print("\n1️⃣ Testing root endpoint...")
try:
    response = requests.get(f"{BASE_URL}/", timeout=5)
    if response.status_code == 200:
        print(f"   ✅ Status: {response.status_code}")
        data = response.json()
        print(f"   Message: {data.get('message')}")
        print(f"   Model loaded: {data.get('model_loaded')}")
    else:
        print(f"   ❌ Status: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Health check
print("\n2️⃣ Testing health endpoint...")
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    if response.status_code == 200:
        print(f"   ✅ Status: {response.status_code}")
        data = response.json()
        print(f"   Health: {data.get('status')}")
    else:
        print(f"   ❌ Status: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Analyze normal text
print("\n3️⃣ Testing analyze endpoint (normal text)...")
try:
    response = requests.post(
        f"{BASE_URL}/api/analyze",
        json={"text": "You are doing an amazing job!"},
        timeout=5
    )
    if response.status_code == 200:
        print(f"   ✅ Status: {response.status_code}")
        data = response.json()
        print(f"   Text: {data.get('text')}")
        print(f"   Prediction: {data.get('prediction')}")
        print(f"   Confidence: {data.get('confidence')}")
    else:
        print(f"   ❌ Status: {response.status_code}")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Analyze hate speech
print("\n4️⃣ Testing analyze endpoint (hate speech)...")
try:
    response = requests.post(
        f"{BASE_URL}/api/analyze",
        json={"text": "I hate you and wish you were dead"},
        timeout=5
    )
    if response.status_code == 200:
        print(f"   ✅ Status: {response.status_code}")
        data = response.json()
        print(f"   Text: {data.get('text')}")
        print(f"   Prediction: {data.get('prediction')}")
        print(f"   Confidence: {data.get('confidence')}")
        print(f"   Category: {data.get('category')}")
    else:
        print(f"   ❌ Status: {response.status_code}")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 5: Multiple predictions
print("\n5️⃣ Testing multiple predictions...")
test_cases = [
    "Have a great day!",
    "You're stupid and worthless",
    "Let's work together",
    "Women belong in the kitchen",
    "Thank you for your help"
]

success_count = 0
for text in test_cases:
    try:
        response = requests.post(
            f"{BASE_URL}/api/analyze",
            json={"text": text},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            pred = data.get('prediction')
            conf = data.get('confidence', 0)
            icon = "🚨" if pred == "Hate Speech" else "✅"
            print(f"   {icon} {text[:40]:40} → {pred:12} ({conf:.3f})")
            success_count += 1
        else:
            print(f"   ❌ Error analyzing: {text[:40]}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

print(f"\n   Successfully analyzed: {success_count}/{len(test_cases)}")

# Test 6: Statistics
print("\n6️⃣ Testing statistics endpoint...")
try:
    response = requests.get(f"{BASE_URL}/api/statistics", timeout=5)
    if response.status_code == 200:
        print(f"   ✅ Status: {response.status_code}")
        data = response.json()
        print(f"   Model accuracy: {data.get('model_accuracy')}")
        print(f"   Status: {data.get('status')}")
    else:
        print(f"   ❌ Status: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*60)
print("✅ API TESTING COMPLETE")
print("="*60 + "\n")
