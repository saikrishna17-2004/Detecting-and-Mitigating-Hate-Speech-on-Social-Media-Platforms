import requests
import json

BASE_URL = "http://localhost:5000/api"

# Test cases covering various categories
test_cases = [
    # Clear hate speech
    {"text": "Kill yourself you loser", "expected": "hate"},
    {"text": "I hate you and wish you were dead", "expected": "hate"},
    {"text": "All Muslims are terrorists", "expected": "hate"},
    {"text": "Fat people are lazy slobs", "expected": "hate"},
    {"text": "You're stupid and worthless", "expected": "hate"},
    {"text": "Go back where you came from", "expected": "hate"},
    {"text": "Old people should die already", "expected": "hate"},
    {"text": "Disabled people are a burden", "expected": "hate"},
    
    # Clear non-hate speech
    {"text": "You are a wonderful person", "expected": "safe"},
    {"text": "Have a great day!", "expected": "safe"},
    {"text": "Thank you so much for your help", "expected": "safe"},
    {"text": "Let's work together on this project", "expected": "safe"},
    {"text": "I appreciate your kindness", "expected": "safe"},
    {"text": "Keep up the good work", "expected": "safe"},
    {"text": "You're very talented", "expected": "safe"},
    {"text": "I love spending time with you", "expected": "safe"},
]

print("\n" + "="*80)
print("TESTING FULL HATE SPEECH DETECTION SYSTEM (ML + Rule-Based)")
print("="*80 + "\n")

correct = 0
total = len(test_cases)

for i, test in enumerate(test_cases, 1):
    try:
        response = requests.post(
            f"{BASE_URL}/analyze",
            json={"text": test["text"]},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            is_hate = result.get("is_hate_speech", False)
            confidence = result.get("confidence", 0)
            detected_type = "hate" if is_hate else "safe"
            
            # Check if prediction matches expected
            is_correct = detected_type == test["expected"]
            correct += 1 if is_correct else 0
            
            status = "✅" if is_correct else "❌"
            
            print(f"{status} Test {i}/{total}: [{detected_type.upper()}] {confidence:.1%} confidence")
            print(f"   Text: \"{test['text']}\"")
            print(f"   Expected: {test['expected'].upper()}, Got: {detected_type.upper()}\n")
        else:
            print(f"❌ Test {i}/{total}: API Error {response.status_code}")
            print(f"   Text: \"{test['text']}\"\n")
            
    except Exception as e:
        print(f"❌ Test {i}/{total}: Exception - {str(e)}")
        print(f"   Text: \"{test['text']}\"\n")

print("="*80)
print(f"RESULTS: {correct}/{total} correct ({correct/total*100:.1f}% accuracy)")
print("="*80 + "\n")
