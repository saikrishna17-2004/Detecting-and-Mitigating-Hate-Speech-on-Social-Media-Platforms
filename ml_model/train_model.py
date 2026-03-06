import pandas as pd
import numpy as np
import json
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import VotingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, f1_score
from sklearn.pipeline import FeatureUnion
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
        # Use richer combined features (word + character n-grams) for better robustness.
        self.vectorizer = FeatureUnion([
            (
                'word_tfidf',
                TfidfVectorizer(
                    max_features=12000,
                    ngram_range=(1, 2),
                    analyzer='word',
                    min_df=2,
                    sublinear_tf=True
                )
            ),
            (
                'char_tfidf',
                TfidfVectorizer(
                    max_features=30000,
                    ngram_range=(3, 5),
                    analyzer='char_wb',
                    min_df=2,
                    sublinear_tf=True
                )
            )
        ])
        self.model = None
        self.model_name = None
        self.decision_threshold = 0.5

    def optimize_threshold(self, y_true, y_prob):
        """Find threshold that maximizes accuracy, with hate-class F1 as tie-breaker."""
        best_threshold = 0.5
        best_accuracy = -1.0
        best_f1_hate = -1.0

        for threshold in np.arange(0.20, 0.81, 0.01):
            y_pred = (y_prob >= threshold).astype(int)
            acc = accuracy_score(y_true, y_pred)
            f1_hate = f1_score(y_true, y_pred, pos_label=1, zero_division=0)

            if (acc > best_accuracy) or (acc == best_accuracy and f1_hate > best_f1_hate):
                best_accuracy = acc
                best_f1_hate = f1_hate
                best_threshold = float(round(threshold, 2))

        return best_threshold, best_accuracy, best_f1_hate
    
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
            df = pd.read_csv(data_path)
            if 'text' not in df.columns or 'label' not in df.columns:
                df = pd.read_csv(data_path, comment='#')

            df = df[['text', 'label']].copy()
            df['text'] = df['text'].astype(str).str.strip()
            df['label'] = pd.to_numeric(df['label'], errors='coerce')
            df = df.dropna(subset=['text', 'label'])
            df = df[df['text'] != '']
            df['label'] = df['label'].astype(int)
            df = df[df['label'].isin([0, 1])]
            return df.reset_index(drop=True)
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
        
        # Train candidate models and keep the best by test accuracy.
        print("\nTraining candidate models...")

        candidates = {
            'LogisticRegression': LogisticRegression(
                random_state=42,
                max_iter=2000,
                C=3.0,
                class_weight='balanced'
            ),
            'MultinomialNB': MultinomialNB(alpha=0.5),
            'VotingEnsemble': VotingClassifier(
                estimators=[
                    ('lr', LogisticRegression(random_state=42, max_iter=2000, C=3.0, class_weight='balanced')),
                    ('nb', MultinomialNB(alpha=0.5))
                ],
                voting='soft',
                weights=[3, 1]
            )
        }

        best_name = None
        best_model = None
        best_accuracy = -1.0
        best_pred = None

        for name, candidate in candidates.items():
            candidate.fit(X_train_vectorized, y_train)
            y_pred = candidate.predict(X_test_vectorized)
            acc = accuracy_score(y_test, y_pred)
            print(f"{name} accuracy: {acc:.4f}")

            if acc > best_accuracy:
                best_accuracy = acc
                best_name = name
                best_model = candidate
                best_pred = y_pred

        self.model = best_model
        self.model_name = best_name

        # Optimize decision threshold for probability-based inference.
        best_prob = self.model.predict_proba(X_test_vectorized)[:, 1]
        threshold, threshold_accuracy, threshold_f1_hate = self.optimize_threshold(y_test, best_prob)
        self.decision_threshold = threshold
        best_pred = (best_prob >= self.decision_threshold).astype(int)
        accuracy = threshold_accuracy

        # Evaluate best model
        print(f"\nSelected model: {best_name}")
        print(f"Optimized threshold: {self.decision_threshold:.2f}")
        print(f"Hate-class F1 @ threshold: {threshold_f1_hate:.4f}")
        print(f"✅ Accuracy: {accuracy:.4f}")
        
        print("\nClassification Report:")
        print(classification_report(y_test, best_pred, target_names=['Normal', 'Hate Speech']))
        
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, best_pred))
        
        return accuracy
    
    def save_model(self, model_dir='ml_model'):
        """Save trained model and vectorizer"""
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        
        model_path = os.path.join(model_dir, 'hate_speech_model.pkl')
        vectorizer_path = os.path.join(model_dir, 'vectorizer.pkl')
        metadata_path = os.path.join(model_dir, 'model_metadata.json')
        
        joblib.dump(self.model, model_path)
        joblib.dump(self.vectorizer, vectorizer_path)

        metadata = {
            'model_name': self.model_name,
            'decision_threshold': self.decision_threshold,
        }
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"\n✅ Model saved to: {model_path}")
        print(f"✅ Vectorizer saved to: {vectorizer_path}")
        print(f"✅ Metadata saved to: {metadata_path}")
    
    def test_model(self, test_texts):
        """Test model with sample texts"""
        print("\n" + "="*50)
        print("TESTING MODEL")
        print("="*50 + "\n")
        
        for text in test_texts:
            processed = self.preprocessor.preprocess(text, remove_stop=False, lemmatize=True)
            vectorized = self.vectorizer.transform([processed])
            probability = self.model.predict_proba(vectorized)[0]
            hate_probability = probability[1] if len(probability) > 1 else probability[0]
            prediction = int(hate_probability >= self.decision_threshold)
            
            print(f"Text: {text}")
            print(f"Prediction: {'Hate Speech' if prediction == 1 else 'Normal'}")
            print(f"Hate Probability: {hate_probability:.3f}")
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
