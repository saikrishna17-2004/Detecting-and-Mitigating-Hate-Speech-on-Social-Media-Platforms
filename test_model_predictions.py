import joblib
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.utils.preprocessing import TextPreprocessor

# Load model and vectorizer
model = joblib.load('ml_model/hate_speech_model.pkl')
vectorizer = joblib.load('ml_model/vectorizer.pkl')
preprocessor = TextPreprocessor()

# Test various samples
test_samples = [
    "You are wonderful",
    "You are amazing",
    "You are a wonderful person",
    "You are terrible",
    "You are a terrible person",
    "You're an inspiration",
    "You're a loser",
    "Thank you so much",
    "I hate you",
    "I love you",
    "You make me happy",
    "You make me sick",
    "Have a great day",
    "Go to hell",
    "You're very kind",
    "You're very stupid",
    "Keep up the good work",
    "Kill yourself",
    "I appreciate you",
    "I despise you"
]

print("\n" + "="*60)
print("TESTING ML MODEL PREDICTIONS")
print("="*60 + "\n")

for text in test_samples:
    # Preprocess
    processed = preprocessor.preprocess(text)
    
    # Vectorize
    features = vectorizer.transform([processed])
    
    # Predict
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0]
    confidence = max(probability)
    
    label = "🔴 HATE" if prediction == 1 else "🟢 SAFE"
    
    print(f"{label} ({confidence:.2%}) | {text}")

print("\n" + "="*60)
