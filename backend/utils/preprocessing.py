import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from langdetect import detect, LangDetectException

# Download required NLTK data
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('punkt')

class TextPreprocessor:
    """Text preprocessing utilities for hate speech detection"""
    
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            nltk.download('stopwords')
            self.stop_words = set(stopwords.words('english'))
    
    def clean_text(self, text):
        """Clean and normalize text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove mentions and hashtags
        text = re.sub(r'@\w+|#\w+', '', text)
        
        # Remove special characters and digits
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\d+', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def remove_stopwords(self, text):
        """Remove stopwords from text"""
        words = text.split()
        filtered_words = [word for word in words if word not in self.stop_words]
        return ' '.join(filtered_words)
    
    def lemmatize_text(self, text):
        """Lemmatize words in text"""
        words = text.split()
        lemmatized_words = [self.lemmatizer.lemmatize(word) for word in words]
        return ' '.join(lemmatized_words)
    
    def preprocess(self, text, remove_stop=True, lemmatize=True):
        """Complete preprocessing pipeline"""
        # Clean text
        text = self.clean_text(text)
        
        # Remove stopwords
        if remove_stop:
            text = self.remove_stopwords(text)
        
        # Lemmatize
        if lemmatize:
            text = self.lemmatize_text(text)
        
        return text
    
    def detect_language(self, text):
        """Detect language of text"""
        try:
            return detect(text)
        except LangDetectException:
            return 'unknown'

# Hate speech categories and keywords
HATE_CATEGORIES = {
    'racial': ['racist', 'racial slur', 'ethnic hatred'],
    'gender': ['sexist', 'misogyny', 'gender-based'],
    'religious': ['religious hatred', 'anti-semitic', 'islamophobic'],
    'homophobic': ['homophobic', 'lgbtq+ hatred'],
    'general': ['offensive', 'abusive', 'threatening']
}

def categorize_hate_speech(text):
    """Categorize hate speech based on keywords"""
    text_lower = text.lower()
    
    # Check for specific categories
    for category, keywords in HATE_CATEGORIES.items():
        for keyword in keywords:
            if keyword in text_lower:
                return category
    
    return 'general'
