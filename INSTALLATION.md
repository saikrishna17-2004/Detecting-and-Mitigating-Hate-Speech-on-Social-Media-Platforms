# Installation and Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (optional)

## Step-by-Step Installation

### 1. Navigate to Project Directory

```powershell
cd c:\Users\nakka\Desktop\pp1
```

### 2. Create Virtual Environment

```powershell
python -m venv .venv
```

### 3. Activate Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If you encounter execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

This will install:
- Flask (Backend framework)
- Streamlit (Frontend framework)
- scikit-learn (Machine Learning)
- transformers (NLP models)
- nltk (Text processing)
- And other required packages

### 5. Download NLTK Data

The system will automatically download required NLTK data on first run. If you want to download manually:

```python
python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('punkt')"
```

### 6. Train the ML Model

```powershell
python ml_model\train_model.py
```

This will:
- Create a sample dataset
- Train an ensemble model (Logistic Regression + Random Forest + Naive Bayes)
- Save the trained model to `ml_model/hate_speech_model.pkl`
- Display accuracy and performance metrics

### 7. Start the Backend API

Open a new terminal and run:

```powershell
.\.venv\Scripts\Activate.ps1
python backend\app.py
```

The API will be available at: `http://localhost:5000`

### 8. Start the Frontend Dashboard

Open another terminal and run:

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run frontend\app.py
```

The dashboard will open automatically in your browser at: `http://localhost:8501`

## Quick Start Script

Alternatively, you can use the automated setup script:

```powershell
.\setup.ps1
```

Then start the services:

```powershell
# Terminal 1 - Backend
.\start_backend.ps1

# Terminal 2 - Frontend
.\start_frontend.ps1
```

## Testing the System

Run the test script to verify everything is working:

```powershell
python test_system.py
```

## Using the Application

### Text Analyzer

1. Navigate to "🔍 Text Analyzer" in the sidebar
2. Enter a User ID and Username
3. Type or paste text to analyze
4. Click "🔍 Analyze Text"
5. View results: detection status, confidence score, category, and action taken

### Dashboard

- View real-time statistics
- Monitor violations by category
- See recent violations
- Track user activity

### User Management

- View all users
- Filter by status (Active/Suspended)
- Manually warn or suspend users
- View user violation history

### Violations Log

- Browse all violations
- Filter by category and action
- Export violations as CSV
- Review detailed violation information

## API Usage

### Analyze Text

```python
import requests

response = requests.post(
    'http://localhost:5000/api/analyze',
    json={
        'text': 'Your text here',
        'user_id': 1,
        'username': 'user1'
    }
)

result = response.json()
print(result)
```

### Get Statistics

```python
response = requests.get('http://localhost:5000/api/statistics')
stats = response.json()
print(stats)
```

### Get Users

```python
response = requests.get('http://localhost:5000/api/users')
users = response.json()
print(users)
```

## Troubleshooting

### Issue: Module Not Found Error

**Solution**: Make sure virtual environment is activated and all packages are installed:
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Issue: Port Already in Use

**Solution**: Kill the process using the port or change the port number:
```powershell
# Find process
netstat -ano | findstr :5000

# Kill process (replace PID with actual process ID)
taskkill /PID <PID> /F
```

### Issue: Database Locked

**Solution**: Close all connections to the database and restart the backend.

### Issue: Model Not Found

**Solution**: Train the model first:
```powershell
python ml_model\train_model.py
```

### Issue: NLTK Data Not Found

**Solution**: Download NLTK data manually:
```python
import nltk
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
```

## Configuration

Edit `.env` file to customize:

- `MAX_WARNINGS`: Number of warnings before suspension (default: 2)
- `AUTO_SUSPEND`: Enable/disable automatic suspension (default: True)
- `SECRET_KEY`: Flask secret key (change in production)
- `DATABASE_URL`: Database connection string

## Production Deployment

For production deployment:

1. Change `SECRET_KEY` and `JWT_SECRET_KEY` in `.env`
2. Use PostgreSQL instead of SQLite
3. Set `FLASK_ENV=production`
4. Use a production WSGI server (e.g., Gunicorn)
5. Enable HTTPS
6. Set up proper logging
7. Configure rate limiting
8. Use a larger, diverse training dataset

## Dataset Recommendations

For better accuracy, train with larger datasets:

- **Twitter Hate Speech Dataset**: ~24,000 tweets
- **Hate Speech and Offensive Language**: ~25,000 tweets
- **HASOC**: Multilingual hate speech dataset
- **Davidson et al. Dataset**: 25K labeled tweets

## Support

For issues or questions:
1. Check this guide
2. Review the README.md
3. Check the code comments
4. Test with test_system.py

## License

This project is licensed under the MIT License.
