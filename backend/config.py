"""
Configuration settings for the hate speech detection system
"""

# API Configuration
API_HOST = 'localhost'
API_PORT = 5000
API_DEBUG = True

# Database Configuration
DATABASE_URL = 'sqlite:///hate_speech_detection.db'

# Model Configuration
MODEL_PATH = 'ml_model/hate_speech_model.pkl'
VECTORIZER_PATH = 'ml_model/vectorizer.pkl'
MODEL_THRESHOLD = 0.5

# Moderation Settings
MAX_WARNINGS = 2
AUTO_SUSPEND = True
SUSPENSION_DURATION_DAYS = 7

# Hate Speech Categories
CATEGORIES = [
    'racial',
    'gender',
    'religious',
    'homophobic',
    'general'
]

# Supported Languages
SUPPORTED_LANGUAGES = ['en', 'es', 'fr', 'de', 'it', 'pt']

# Feature Flags
ENABLE_MULTILINGUAL = True
ENABLE_CONTEXT_FILTERING = True
LOG_ALL_POSTS = True
