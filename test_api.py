import requests
import json
import time

BASE_URL = "http://localhost:5000"

print("\n" + "="*80)
print("🧪 TESTING HATE SPEECH DETECTION API")
print("="*80 + "\n")

# Test 1: Root endpoint
print("Test 1: Checking API root endpoint...")
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"✅ Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}\n")
except Exception as e:
    print(f"❌ Error: {e}\n")

# Test 2: Analyze normal text
print("Test 2: Analyzing normal text...")
test_texts = [
    "You are doing an amazing job!",
    "Have a great day everyone!",
    "Let's work together on this project",
    "Thank you for your support"
]

for text in test_texts:
    try:
        start = time.time()
        response = requests.post(
            f"{BASE_URL}/api/analyze",
            json={"text": text}
        )
        elapsed = (time.time() - start) * 1000
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Text: {text[:50]}...")
            print(f"   Prediction: {result.get('prediction', 'N/A')}")
            print(f"   Confidence: {result.get('confidence', 0):.3f}")
            print(f"   Response time: {elapsed:.1f}ms\n")
        else:
            print(f"❌ Error {response.status_code}: {response.text}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")

# Test 3: Analyze hate speech
print("\nTest 3: Analyzing hate speech...")
hate_texts = [
    "I hate you and wish you were dead",
    "You're worthless and should die",
    "Your race is subhuman trash",
    "Kill yourself you pathetic loser",
    "Women belong in the kitchen",
    "Gay people are mentally ill",
    "Old people are useless burdens",
    "Fat people disgust me"
]

for text in hate_texts:
    try:
        start = time.time()
        response = requests.post(
            f"{BASE_URL}/api/analyze",
            json={"text": text}
        )
        elapsed = (time.time() - start) * 1000
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Text: {text[:50]}...")
            print(f"   Prediction: {result.get('prediction', 'N/A')}")
            print(f"   Confidence: {result.get('confidence', 0):.3f}")
            print(f"   Category: {result.get('category', 'N/A')}")
            print(f"   Response time: {elapsed:.1f}ms\n")
        else:
            print(f"❌ Error {response.status_code}: {response.text}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")

# Test 4: Get statistics
print("\nTest 4: Getting platform statistics...")
try:
    response = requests.get(f"{BASE_URL}/api/statistics")
    if response.status_code == 200:
        stats = response.json()
        print(f"✅ Status: {response.status_code}")
        print(f"   Statistics: {json.dumps(stats, indent=2)}\n")
    else:
        print(f"❌ Error {response.status_code}: {response.text}\n")
except Exception as e:
    print(f"❌ Error: {e}\n")

# Test 5: Batch analysis
print("\nTest 5: Batch analysis performance test...")
batch_texts = [
    "Hello world",
    "I hate you",
    "Nice weather today",
    "You're stupid",
    "Thank you so much",
    "Die you scum",
    "Great work everyone",
    "All people from that religion are evil"
]

print(f"Analyzing {len(batch_texts)} texts in batch...")
start_batch = time.time()
results = []

for text in batch_texts:
    try:
        response = requests.post(
            f"{BASE_URL}/api/analyze",
            json={"text": text}
        )
        if response.status_code == 200:
            results.append(response.json())
    except Exception as e:
        print(f"Error analyzing '{text}': {e}")

elapsed_batch = (time.time() - start_batch) * 1000

print(f"\n✅ Batch analysis complete!")
print(f"   Total time: {elapsed_batch:.1f}ms")
print(f"   Average per text: {elapsed_batch/len(batch_texts):.1f}ms")
print(f"   Throughput: {len(batch_texts)/(elapsed_batch/1000):.1f} texts/second\n")

# Summary
hate_count = sum(1 for r in results if r.get('prediction') == 'Hate Speech')
normal_count = len(results) - hate_count

print(f"📊 Batch Results Summary:")
print(f"   Total analyzed: {len(results)}")
print(f"   Hate speech detected: {hate_count}")
print(f"   Normal speech: {normal_count}\n")

for i, (text, result) in enumerate(zip(batch_texts, results), 1):
    pred = result.get('prediction', 'N/A')
    conf = result.get('confidence', 0)
    icon = "🚨" if pred == "Hate Speech" else "✅"
    print(f"   {icon} [{i}] {text[:40]:40} → {pred:15} ({conf:.3f})")

print("\n" + "="*80)
print("✅ API TESTING COMPLETE")
print("="*80 + "\n")
