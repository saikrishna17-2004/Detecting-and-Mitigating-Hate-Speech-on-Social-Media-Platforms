# Project Structure

```
pp1/
│
├── backend/                          # Backend API
│   ├── __init__.py
│   ├── app.py                       # Flask application entry point
│   ├── database.py                  # Database models (User, Violation, Post)
│   ├── config.py                    # Configuration settings
│   │
│   ├── models/                      # ML models
│   │   ├── __init__.py
│   │   └── detector.py             # Hate speech detector class
│   │
│   ├── routes/                      # API endpoints
│   │   ├── __init__.py
│   │   └── api.py                  # API routes (analyze, users, violations, stats)
│   │
│   └── utils/                       # Utility functions
│       ├── __init__.py
│       ├── preprocessing.py        # Text preprocessing utilities
│       └── helpers.py              # Helper functions
│
├── frontend/                         # Frontend Dashboard
│   ├── __init__.py
│   └── app.py                       # Streamlit dashboard application
│
├── ml_model/                         # Machine Learning
│   ├── __init__.py
│   ├── train_model.py              # Model training script
│   ├── hate_speech_model.pkl       # Trained model (generated)
│   └── vectorizer.pkl              # TF-IDF vectorizer (generated)
│
├── data/                            # Data files
│   └── sample_data.csv             # Sample training dataset
│
├── .venv/                           # Virtual environment (generated)
│
├── instance/                        # Flask instance folder (generated)
│   └── hate_speech_detection.db   # SQLite database (generated)
│
├── .env                            # Environment variables
├── requirements.txt                # Python dependencies
├── README.md                       # Project overview
├── INSTALLATION.md                 # Installation guide
├── PROJECT_STRUCTURE.md            # This file
│
├── setup.ps1                       # Quick setup script
├── start_backend.ps1               # Start backend server
├── start_frontend.ps1              # Start frontend dashboard
└── test_system.py                  # System test script
```

## Component Details

### Backend (Flask API)

#### `app.py`
- Main Flask application
- Initializes database and registers routes
- Provides root endpoint with API information

#### `database.py`
- SQLAlchemy ORM models:
  - **User**: Tracks social media users, warnings, suspension status
  - **Violation**: Records hate speech incidents with category and confidence
  - **Post**: Stores all analyzed content

#### `models/detector.py`
- `HateSpeechDetector` class
- Loads trained ML model
- Analyzes text and returns:
  - Hate speech prediction (True/False)
  - Confidence score (0-1)
  - Category (racial, gender, religious, etc.)
  - Detected language

#### `routes/api.py`
API endpoints:
- `POST /api/analyze` - Analyze text for hate speech
- `GET /api/users` - Get all users
- `GET /api/users/<id>` - Get specific user details
- `POST /api/users/<id>/warn` - Warn a user
- `POST /api/users/<id>/suspend` - Suspend a user
- `POST /api/users/<id>/unsuspend` - Unsuspend a user
- `GET /api/violations` - Get all violations (with pagination)
- `GET /api/statistics` - Get platform statistics

#### `utils/preprocessing.py`
- `TextPreprocessor` class:
  - Text cleaning (URLs, mentions, special chars)
  - Stopword removal
  - Lemmatization
  - Language detection
- `categorize_hate_speech()` function

#### `config.py`
Configuration constants:
- API settings
- Database URL
- Model paths
- Moderation settings
- Feature flags

### Frontend (Streamlit Dashboard)

#### `app.py`
Multi-page Streamlit application:

**Pages:**
1. **Dashboard** (🏠)
   - Key metrics (users, violations, posts)
   - Pie chart: Clean vs Hate Speech posts
   - Bar chart: Violations by category
   - Recent violations table

2. **Text Analyzer** (🔍)
   - Real-time text analysis
   - User input (ID, username, text)
   - Results display with confidence score
   - Action feedback (warning/suspension)

3. **User Management** (👥)
   - User list with filters
   - Sort and search functionality
   - Manual moderation actions:
     - Warn user
     - Suspend user
     - Unsuspend user
   - User details and violation history

4. **Violations Log** (📊)
   - Complete violations table
   - Filter by category and action
   - Pagination support
   - CSV export functionality

5. **About** (ℹ️)
   - System overview
   - Feature descriptions
   - Technology stack
   - How it works
   - System status check

### ML Model

#### `train_model.py`
- `HateSpeechModelTrainer` class
- Creates or loads training dataset
- Text preprocessing pipeline
- Trains ensemble model:
  - Logistic Regression
  - Random Forest
  - Multinomial Naive Bayes
  - Voting Classifier (soft voting)
- TF-IDF vectorization
- Model evaluation and metrics
- Saves trained model and vectorizer

### Database Schema

#### Users Table
```
- id (Integer, Primary Key)
- username (String, Unique)
- email (String, Unique)
- warning_count (Integer)
- is_suspended (Boolean)
- suspended_at (DateTime)
- created_at (DateTime)
```

#### Violations Table
```
- id (Integer, Primary Key)
- user_id (Foreign Key → users.id)
- content (Text)
- category (String)
- confidence_score (Float)
- language (String)
- timestamp (DateTime)
- action_taken (String)
```

#### Posts Table
```
- id (Integer, Primary Key)
- user_id (Foreign Key → users.id)
- content (Text)
- is_hate_speech (Boolean)
- confidence_score (Float)
- created_at (DateTime)
```

## Data Flow

### Analysis Request Flow

1. **User Input** → Frontend form (Text Analyzer page)
2. **API Request** → `POST /api/analyze` with text, user_id, username
3. **Preprocessing** → Clean and normalize text
4. **Detection** → ML model predicts hate speech
5. **Database** → Record violation (if hate speech detected)
6. **User Update** → Increment warnings, check suspension threshold
7. **Response** → Return results with action taken
8. **Display** → Show results on frontend

### Statistics Flow

1. **Request** → Frontend Dashboard or API call
2. **Query** → Aggregate data from database
3. **Calculate** → Compute metrics and percentages
4. **Response** → Return statistics JSON
5. **Visualize** → Display charts and metrics

## Key Features

### Automated Moderation
- Warning system with configurable threshold
- Automatic suspension after max warnings
- Manual moderation override options

### Categorization
- Racial hate speech
- Gender-based discrimination
- Religious intolerance
- Homophobic content
- General offensive language

### Multilingual Support
- Language detection using langdetect
- Support for multiple languages
- Extensible to additional languages

### Performance Monitoring
- Real-time statistics
- Violation tracking
- User behavior analytics
- Category-wise breakdown

## Extension Points

### Adding New Categories
1. Update `HATE_CATEGORIES` in `utils/preprocessing.py`
2. Update `CATEGORIES` in `config.py`
3. Retrain model with labeled examples

### Adding New Languages
1. Update `SUPPORTED_LANGUAGES` in `config.py`
2. Train model with multilingual dataset
3. Update preprocessing to handle language-specific rules

### Custom Actions
1. Add new action logic in `routes/api.py`
2. Update database schema if needed
3. Add UI controls in frontend

### Integration
- Use API endpoints to integrate with existing platforms
- Webhook support can be added for real-time notifications
- Batch processing endpoint can be added for bulk analysis

## Security Considerations

- Input validation and sanitization
- SQL injection prevention (SQLAlchemy ORM)
- XSS protection
- Rate limiting (add in production)
- Authentication/Authorization (JWT ready)
- HTTPS in production
- Environment variable for secrets

## Performance Optimization

- Database indexing on frequently queried fields
- Caching for statistics
- Batch processing for multiple texts
- Model optimization (quantization, distillation)
- Connection pooling
- Asynchronous processing for heavy tasks

## Testing

- Unit tests for preprocessing
- API endpoint tests
- Model accuracy evaluation
- Integration tests
- Load testing for production

## Monitoring

- Application logs
- Error tracking
- Performance metrics
- User activity analytics
- Model performance monitoring
