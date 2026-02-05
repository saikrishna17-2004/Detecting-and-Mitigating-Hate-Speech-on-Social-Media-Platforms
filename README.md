# Hate Speech Detection & Mitigation System

A full-stack Python application for detecting and mitigating hate speech on social media platforms using NLP and Machine Learning.

## Features

- **Real-time Hate Speech Detection**: Analyzes user content using trained ML models
- **Automated User Management**: Warning system and automatic suspension after violations
- **Moderation Dashboard**: Comprehensive admin panel for monitoring and management
- **Multilingual Support**: Detects hate speech in multiple languages
- **Categorization**: Classifies hate speech (racial, gender-based, religious, etc.)
- **Behavioral Tracking**: Logs all offenses with timestamps and user history
- **REST API**: Backend API for integration with social platforms

## Tech Stack

### Backend
- **Framework**: Flask
- **Database**: SQLite (can be upgraded to PostgreSQL)
- **ML Libraries**: scikit-learn, transformers (BERT), nltk
- **Authentication**: Flask-JWT-Extended

### Frontend
- **Framework**: Streamlit (for rapid development)
- **Visualization**: Plotly, Matplotlib

### ML Model
- **Approach**: BERT-based transformer model + traditional ML (ensemble)
- **Dataset**: Hate speech datasets (Twitter, Reddit)

## Project Structure

```
pp1/
├── backend/
│   ├── app.py                 # Flask application
│   ├── models/                # ML models
│   ├── routes/                # API endpoints
│   ├── utils/                 # Utility functions
│   └── database.py            # Database models
├── frontend/
│   ├── app.py                 # Streamlit app
│   ├── pages/                 # Dashboard pages
│   └── components/            # Reusable components
├── ml_model/
│   ├── train_model.py         # Model training script
│   ├── preprocessing.py       # Text preprocessing
│   └── model.pkl              # Trained model
├── data/
│   └── sample_data.csv        # Sample dataset
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository
2. Create virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Train the ML Model
```bash
python ml_model/train_model.py
```

### 2. Run Backend API
```bash
python backend/app.py
```
Backend will run on `http://localhost:5000`

### 3. Run Frontend Dashboard
```bash
streamlit run frontend/app.py
```
Frontend will run on `http://localhost:8501`

## API Endpoints

- `POST /api/analyze` - Analyze text for hate speech
- `GET /api/users` - Get all users
- `GET /api/users/<id>` - Get user details
- `POST /api/users/<id>/warn` - Issue warning to user
- `POST /api/users/<id>/suspend` - Suspend user
- `GET /api/violations` - Get all violations
- `GET /api/statistics` - Get platform statistics

## License

MIT License
