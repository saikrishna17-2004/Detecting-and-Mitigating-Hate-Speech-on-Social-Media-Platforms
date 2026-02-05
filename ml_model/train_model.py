import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.utils.preprocessing import TextPreprocessor

class HateSpeechModelTrainer:
    """Train hate speech detection model"""
    
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        # Increase capacity and use sublinear TF; keep word ngrams
        self.vectorizer = TfidfVectorizer(
            max_features=10000,
            ngram_range=(1, 2),
            analyzer='word',
            sublinear_tf=True
        )
        self.model = None
    
    def create_sample_dataset(self):
        """Create a sample dataset for training"""
        # Sample hate speech examples
        hate_speech_samples = [
            "You are stupid and worthless",
            "I hate all people from that country",
            "You should die",
            "Go back to where you came from",
            "Women are inferior and stupid",
            "All members of that religion are terrorists",
            "You are trash and garbage",
            "Kill yourself you loser",
            "I wish you would just disappear",
            "Your kind doesn't belong here",
            "You're an idiot and a failure",
            "Nobody wants you around",
            "You deserve to suffer",
            "Pathetic loser go away",
            "You're disgusting and worthless",
            "I hope bad things happen to you",
            "Your people are all criminals",
            "You make me sick",
            "The world would be better without you",
            "You're a waste of space",
            # Single-word profanity for explicit signal
            "fuck",
            # Profanity-focused abusive phrases
            "fuck you",
            "you fucking idiot",
            "shut the fuck up",
            "you piece of shit",
            "what a bitch",
            "you bastard",
            "asshole",
            "fucking loser",
            "you are fucking trash",
            "go fuck yourself"
        ]
        
        # Load additional lexicon terms (if present) to synthesize abusive phrases
        lexicon_path = 'data/hate_keywords.txt'
        lexicon_terms = []
        if os.path.exists(lexicon_path):
            with open(lexicon_path, 'r', encoding='utf-8') as f:
                for line in f:
                    term = line.strip().lower()
                    if not term or term.startswith('#'):
                        continue
                    lexicon_terms.append(term)

        # Synthesize abusive phrases from terms (limit to avoid explosion)
        synthesized = []
        max_synth = 2000  # cap to keep dataset size reasonable
        for term in lexicon_terms:
            if ' ' in term:
                synthesized.append(term)
            else:
                synthesized.extend([
                    f"you {term}",
                    f"you are {term}",
                    f"such a {term}",
                    f"{term} behavior",
                ])
            if len(synthesized) >= max_synth:
                break

        # Deduplicate and extend hate samples
        if synthesized:
            deduped = list(dict.fromkeys(synthesized))
            hate_speech_samples.extend(deduped)

        # Sample normal speech examples
        normal_speech_samples = [
            "Have a great day!",
            "I disagree with your opinion but respect your view",
            "That's an interesting perspective",
            "Can we discuss this topic further?",
            "I enjoyed reading your post",
            "Thanks for sharing this information",
            "Looking forward to your next update",
            "Great work on this project",
            "I appreciate your effort",
            "This is a helpful contribution",
            "Nice to meet you",
            "How are you doing today?",
            "I'm excited about this opportunity",
            "Let's work together on this",
            "Your ideas are creative",
            "I learned something new today",
            "This community is welcoming",
            "Thank you for your help",
            "I hope you have a wonderful time",
            "Keep up the good work"
        ]
        
        # Combine and label
        texts = hate_speech_samples + normal_speech_samples
        labels = [1] * len(hate_speech_samples) + [0] * len(normal_speech_samples)
        
        # Create DataFrame
        df = pd.DataFrame({
            'text': texts,
            'label': labels
        })
        
        return df
    
    def load_or_create_data(self, data_path='data/hate_speech_dataset.csv'):
        """Load existing dataset or create sample data"""
        if os.path.exists(data_path):
            print(f"Loading dataset from {data_path}")
            return pd.read_csv(data_path, comment='#')
        else:
            print("Creating sample dataset...")
            return self.create_sample_dataset()
    
    def preprocess_data(self, df):
        """Preprocess text data"""
        print("Preprocessing text data...")
        df['processed_text'] = df['text'].apply(
            lambda x: self.preprocessor.preprocess(x, remove_stop=False, lemmatize=True)
        )
        return df
    
    def train(self, df):
        """Train the model"""
        print("\n" + "="*50)
        print("TRAINING HATE SPEECH DETECTION MODEL")
        print("="*50 + "\n")
        
        # Preprocess
        df = self.preprocess_data(df)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            df['processed_text'], df['label'],
            test_size=0.2,
            random_state=42,
            stratify=df['label']
        )
        
        print(f"Training samples: {len(X_train)}")
        print(f"Testing samples: {len(X_test)}")
        
        # Vectorize text
        print("\nVectorizing text...")
        X_train_vectorized = self.vectorizer.fit_transform(X_train)
        X_test_vectorized = self.vectorizer.transform(X_test)
        
        # Create ensemble model
        print("\nTraining ensemble model...")
        
        # Individual models
        lr = LogisticRegression(random_state=42, max_iter=1000)
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        nb = MultinomialNB()
        
        # Ensemble voting classifier
        self.model = VotingClassifier(
            estimators=[('lr', lr), ('rf', rf), ('nb', nb)],
            voting='soft'
        )
        
        # Train
        self.model.fit(X_train_vectorized, y_train)
        
        # Evaluate
        print("\nEvaluating model...")
        y_pred = self.model.predict(X_test_vectorized)
        
        accuracy = accuracy_score(y_test, y_pred)
        print(f"\n✅ Accuracy: {accuracy:.4f}")
        
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Normal', 'Hate Speech']))
        
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        
        return accuracy
    
    def save_model(self, model_dir='ml_model'):
        """Save trained model and vectorizer"""
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        
        model_path = os.path.join(model_dir, 'hate_speech_model.pkl')
        vectorizer_path = os.path.join(model_dir, 'vectorizer.pkl')
        
        joblib.dump(self.model, model_path)
        joblib.dump(self.vectorizer, vectorizer_path)
        
        print(f"\n✅ Model saved to: {model_path}")
        print(f"✅ Vectorizer saved to: {vectorizer_path}")
    
    def test_model(self, test_texts):
        """Test model with sample texts"""
        print("\n" + "="*50)
        print("TESTING MODEL")
        print("="*50 + "\n")
        
        for text in test_texts:
            processed = self.preprocessor.preprocess(text, remove_stop=False, lemmatize=True)
            vectorized = self.vectorizer.transform([processed])
            prediction = self.model.predict(vectorized)[0]
            probability = self.model.predict_proba(vectorized)[0]
            
            print(f"Text: {text}")
            print(f"Prediction: {'Hate Speech' if prediction == 1 else 'Normal'}")
            print(f"Confidence: {max(probability):.3f}")
            print("-" * 50)

def main():
    """Main training function"""
    print("\n🚀 Starting Hate Speech Detection Model Training...\n")
    
    # Create trainer
    trainer = HateSpeechModelTrainer()
    
    # Load data from sample_data.csv (use absolute path from script location)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(os.path.dirname(script_dir), 'data', 'sample_data.csv')
    df = trainer.load_or_create_data(data_path=data_path)
    print(f"\nDataset shape: {df.shape}")
    print(f"Hate speech samples: {df['label'].sum()}")
    print(f"Normal speech samples: {(df['label'] == 0).sum()}")
    
    # Train model
    accuracy = trainer.train(df)
    
    # Save model
    trainer.save_model()
    
    # Test with sample texts
    test_texts = [
        "You are a wonderful person!",
        "I hate you and wish you were dead",
        "Let's work together on this project",
        "You're stupid and worthless",
        "Have a great day!"
    ]
    
    trainer.test_model(test_texts)
    
    print("\n✅ Training completed successfully!")
    print("You can now use the model in the backend API.\n")

if __name__ == "__main__":
    main()
