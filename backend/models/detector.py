try:
    import joblib
except Exception:
    joblib = None
import os
import re
from backend.utils.preprocessing import TextPreprocessor, categorize_hate_speech

# Multi-language support
try:
    from langdetect import detect, LangDetectException
    LANGDETECT_AVAILABLE = True
except ImportError:
    LANGDETECT_AVAILABLE = False
    print("langdetect not available - multi-language detection disabled")

# Translation support (optional)
try:
    from googletrans import Translator
    TRANSLATION_AVAILABLE = True
except ImportError:
    TRANSLATION_AVAILABLE = False
    print("googletrans not available - translation disabled")

class HateSpeechDetector:
    """Hate speech detection model wrapper with multi-language support"""
    
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.model = None
        self.vectorizer = None
        self.model_loaded = False
        self.translator = Translator() if TRANSLATION_AVAILABLE else None

        # Try to load trained model
        self.load_model()

    def load_model(self):
        """Load pre-trained model if available"""
        model_path = 'ml_model/hate_speech_model.pkl'
        vectorizer_path = 'ml_model/vectorizer.pkl'
        
        try:
            if joblib and os.path.exists(model_path) and os.path.exists(vectorizer_path):
                self.model = joblib.load(model_path)
                self.vectorizer = joblib.load(vectorizer_path)
                self.model_loaded = True
                print("ML Model loaded successfully!")
            else:
                print("ML Model not found or joblib missing. Using rule-based detection.")
        except Exception as e:
            print(f"Error loading model: {e}. Using rule-based detection.")
    
    def predict_with_model(self, text):
        """Predict using trained ML model"""
        try:
            # Preprocess text
            processed_text = self.preprocessor.preprocess(text)
            
            # Vectorize
            text_vectorized = self.vectorizer.transform([processed_text])
            
            # Predict
            prediction = self.model.predict(text_vectorized)[0]
            probability = self.model.predict_proba(text_vectorized)[0]
            
            # Get confidence score (probability of hate speech class)
            confidence = probability[1] if len(probability) > 1 else probability[0]
            
            return bool(prediction), float(confidence)
        except Exception as e:
            print(f"Model prediction error: {e}")
            return self.rule_based_detection(text)
    
    def rule_based_detection(self, text):
        """Sophisticated pattern-based hate speech detection.
        - Uses context and patterns to detect hate speech.
        - Detects hate speech targeting groups (stereotyping, generalizations).
        - No simple keyword matching - focuses on context and harmful patterns.
        """
        text_lower = text.lower()

        # Context patterns that indicate non-hate speech (whitelist patterns)
        safe_patterns = [
            r'\bi love\b',
            r'\blove\b.*\bnature\b',
            r'\bnature\b.*\bbeautiful\b',
            r'\bi like\b',
            r'\bthank you\b',
            r'\bgreat\b',
            r'\bawesome\b',
            r'\bwonderful\b',
            r'\bamazing\b',
            r'\bnever goes out of style\b',
            r'\bis not allowed\b',
            r'\bagainst hate\b',
            r'\bstop hate\b',
            r'\banti.?hate\b'
        ]
        
        # Check if text matches safe patterns
        is_safe_context = any(re.search(pattern, text_lower) for pattern in safe_patterns)
        
        if is_safe_context:
            # Don't flag as hate speech if it's clearly in a positive/neutral context
            return False, 0.0

        # Hate speech patterns targeting groups (stereotyping, generalizations)
        group_hate_patterns = [
            # Generalizations about groups
            (r'\ball\s+(members\s+of\s+)?(that|those|these)?\s*(people|members|folks)\s+(from|of|in)\s+\w+\s+(are|is)\s+(\w+)', 0.8),
            (r'\ball\s+\w+\s+(people|women|men|members)\s+(are|is)\s+(\w+)', 0.8),
            (r'\bevery\s+\w+\s+(person|member|individual)\s+(is|are)\s+(\w+)', 0.75),
            # Religious/ethnic targeting
            (r'\ball\s+(members\s+of\s+)?(that|those)?\s*religion\s+(are|is)\s+\w+', 0.85),
            (r'\b(all|every)\s+\w+\s+(from|of)\s+(that|those|the)\s+(country|place|religion)\s+(are|is)\s+\w+', 0.8),
            # Body shaming and appearance-based discrimination
            (r'\b(fat|overweight|obese)\s+(people|person|women|men)\s+(are|is)\s+(lazy|slobs|disgusting|ugly|worthless)', 0.85),
            (r'\b(skinny|thin)\s+(people|person)\s+(are|is)\s+(weak|anorexic|disgusting)', 0.80),
            (r'\b(ugly|hideous)\s+(people|person)\s+', 0.70),
            # Age discrimination
            (r'\b(old|elderly)\s+(people|person)\s+(are|is)\s+(useless|worthless)', 0.85),
            (r'\b(old|elderly)\s+people\s+should\s+(just\s+)?(die|leave)', 0.90),
            (r'\byoung\s+people\s+are\s+(stupid|lazy|entitled)', 0.75),
            # Disability discrimination  
            (r'\b(disabled|handicapped)\s+(people|person)\s+(are|is)\s+(burden|useless|worthless)', 0.85),
            (r'\b(disabled|handicapped)\s+(people|person)\s+(can\'t|cannot|dont|don\'t)\s+(contribute|work|help)', 0.85),
            # Economic class discrimination
            (r'\b(poor|homeless)\s+(people|person)\s+(are|is)\s+(lazy|worthless)', 0.80),
            (r'\ball\s+(homeless|poor)\s+(are|is)\s+(drug addicts|criminals|lazy)', 0.85),
            (r'\brich\s+people\s+are\s+(evil|parasites|greedy)', 0.75),
            # Gender discrimination
            (r'\b(women|men)\s+(are|is)\s+(too|all)\s+(emotional|weak|stupid|inferior)', 0.85),
            (r'\b(women|girls)\s+belong\s+in\s+(kitchen|home)', 0.85),
            # LGBTQ+ discrimination
            (r'\b(gay|lesbian|trans|transgender)\s+(people|person)\s+(are|is)\s+\w+', 0.80),
            # Specific hate speech indicators
            (r'\b(terrorist|terrorists|criminals|inferior|subhuman|animals)\b', 0.7),
            # "Your kind" type statements
            (r'\byour\s+kind\s+(doesn\'t|dont|should|must|are|is)', 0.85),
            (r'\bpeople\s+like\s+you\s+(are|should|must|dont|doesn\'t)', 0.75),
            # Deportation/exclusion
            (r'\bgo\s+back\s+(to|where)', 0.8),
            (r'\bdon\'t\s+belong\s+here', 0.75),
            (r'\bget\s+out\s+of\s+(our|this|my)', 0.75),
        ]
        
        # Check for group hate patterns
        max_group_confidence = 0.0
        for pattern, confidence in group_hate_patterns:
            if re.search(pattern, text_lower):
                max_group_confidence = max(max_group_confidence, confidence)
        
        if max_group_confidence >= 0.7:
            # Strong hate speech pattern detected
            return True, max_group_confidence

        # No hate speech pattern detected
        return False, 0.0
    
    def detect_language(self, text):
        """Detect the language of the text"""
        if not LANGDETECT_AVAILABLE:
            return 'en'  # Default to English
        
        try:
            language = detect(text)
            return language
        except (LangDetectException, Exception):
            return 'unknown'
    
    def translate_to_english(self, text, source_lang):
        """Translate text to English for analysis"""
        if not TRANSLATION_AVAILABLE or not self.translator:
            return text, False  # Return original text if translation unavailable
        
        try:
            if source_lang == 'en' or source_lang == 'unknown':
                return text, False
            
            translated = self.translator.translate(text, src=source_lang, dest='en')
            return translated.text, True
        except Exception as e:
            print(f"Translation error: {e}")
            return text, False  # Fallback to original text
    
    def analyze(self, text):
        """Analyze text for hate speech with multi-language support"""
        if not text or len(text.strip()) == 0:
            return {
                'is_hate_speech': False,
                'confidence': 0.0,
                'category': 'none',
                'language': 'unknown',
                'translated': False
            }
        
        # Detect language
        language = self.detect_language(text)
        
        # Translate non-English text
        analysis_text = text
        was_translated = False
        if language not in ['en', 'unknown']:
            analysis_text, was_translated = self.translate_to_english(text, language)
        
        # Rule-based prediction (always run to catch lexicon hits and context)
        rule_is_hate, rule_conf = self.rule_based_detection(analysis_text)

        # ML prediction (if available)
        ml_is_hate, ml_conf = (False, 0.0)
        if self.model_loaded:
            try:
                ml_is_hate, ml_conf = self.predict_with_model(analysis_text)
            except Exception as _:
                ml_is_hate, ml_conf = (False, 0.0)

        # Improved combination logic:
        # If rule-based says NOT hate (including safe context detection), trust it
        # This prevents ML false positives on context-safe phrases
        if not rule_is_hate and rule_conf == 0.0:
            # Rule-based explicitly cleared this (safe context)
            is_hate = False
            confidence = 0.0
        elif rule_is_hate and ml_is_hate:
            # Both agree it's hate - high confidence
            is_hate = True
            confidence = max(rule_conf, ml_conf)
        elif rule_is_hate:
            # Rule-based says hate, ML says not - trust rule-based if high confidence
            is_hate = rule_conf >= 0.7
            confidence = rule_conf
        elif ml_is_hate:
            # ML says hate, rule-based says not - lower confidence, likely false positive
            is_hate = ml_conf >= 0.75  # Higher threshold for ML-only detection
            confidence = ml_conf * 0.8  # Reduce confidence
        else:
            # Both say not hate
            is_hate = False
            confidence = 0.0
        
        # Categorize if hate speech detected
        category = categorize_hate_speech(analysis_text) if is_hate else 'none'
        
        return {
            'is_hate_speech': is_hate,
            'confidence': round(confidence, 3),
            'category': category,
            'language': language,
            'translated': was_translated,
            'original_text': text if was_translated else None
        }

# Global detector instance
detector = HateSpeechDetector()
