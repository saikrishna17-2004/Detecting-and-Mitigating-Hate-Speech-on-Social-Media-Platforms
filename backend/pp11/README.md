# Hate Speech Detection - Full Stack Social Media Platform 🚀

## 🌟 Project Overview

A complete full-stack social media application with **Instagram-like UI** and **real-time AI-powered hate speech detection**. The system automatically moderates content, warns users, and suspends accounts after repeated violations.

---

## 🎯 Features

### 👥 User Features
- ✅ User registration & authentication
- ✅ Create posts with text and images
- ✅ Like and comment on posts
- ✅ Instagram-style news feed
- ✅ User profiles with stats
- ✅ Real-time moderation alerts

### 🛡️ Moderation System
- ✅ AI-powered hate speech detection (87.5% accuracy)
- ✅ Automatic content flagging
- ✅ Progressive warning system
- ✅ Account suspension after 3 violations
- ✅ Category classification (racism, sexism, toxicity, etc.)

### 👨‍💼 Admin Dashboard
- ✅ User management (warn, suspend, unsuspend)
- ✅ Violation monitoring
- ✅ Real-time statistics
- ✅ Platform analytics

---

## 🏗️ Technology Stack

### Backend
- **Framework:** Flask 3.0.0
- **Database:** SQLite + SQLAlchemy 2.0.44
- **ML Model:** scikit-learn 1.7.2 (Ensemble: Logistic Regression + Random Forest + Naive Bayes)
- **NLP:** NLTK 3.8.1, TF-IDF Vectorizer
- **Deep Learning:** Transformers 4.57.1, PyTorch 2.9.0

### Frontend
- **Framework:** React 18.2.0
- **UI Library:** Material-UI 5.14.0
- **Routing:** React Router 6.20.0
- **HTTP Client:** Axios 1.6.0
- **Styling:** Emotion (CSS-in-JS)

### Python Environment
- **Version:** Python 3.13.8
- **Virtual Environment:** `.venv`

---

## 📂 Project Structure

```
pp11/
├── backend/
│   ├── app.py                  # Flask application entry point
│   ├── database.py             # SQLAlchemy models (User, Post, Violation)
│   ├── routes/
│   │   └── api.py             # REST API endpoints
│   ├── models/
│   │   └── detector.py        # ML hate speech detector
│   └── utils/
│       ├── preprocessing.py   # Text preprocessing
│       └── response.py        # API response helpers
│
├── frontend-react/             # Instagram-like UI
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── index.js           # App entry point
│   │   ├── App.js             # Main app with routing
│   │   ├── services/
│   │   │   └── api.js         # API service layer
│   │   └── components/
│   │       ├── auth/          # Login, Register
│   │       ├── posts/         # Feed, PostCard, CreatePost
│   │       ├── profile/       # User profile page
│   │       ├── admin/         # Admin dashboard
│   │       ├── layout/        # Navbar
│   │       └── moderation/    # Moderation alerts
│   └── package.json
│
├── ml_model/
│   ├── train_model.py         # Model training script
│   ├── hate_speech_model.pkl  # Trained model (87.5% accuracy)
│   └── vectorizer.pkl         # TF-IDF vectorizer
│
├── data/
│   └── hate_speech_dataset.csv
│
├── .env                       # Environment variables
├── requirements.txt           # Python dependencies
├── QUICK_START.md            # Quick start guide
└── README.md                 # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.13.8
- Node.js & npm
- Virtual environment activated

### 1️⃣ Start Backend API

```powershell
# In Terminal 1
python app.py
```
✅ Backend runs on: **http://localhost:5000**

### 2️⃣ Start React Frontend

```powershell
# In Terminal 2
cd frontend-react
npm start
```
✅ Frontend runs on: **http://localhost:3000**

### 3️⃣ Access the Application
- Open your browser to: **http://localhost:3000**
- Register a new account
- Start posting!

---

## 🎮 How to Use

### Creating Posts
1. Type your caption in the text area
2. Add an image URL (optional)
3. Click "Post"
4. ⚠️ If hate speech is detected, you'll receive a warning

### Moderation Policy
- **1st Offense:** ⚠️ Warning
- **2nd Offense:** ⚠️ Final warning  
- **3rd Offense:** 🚫 Account suspended (configurable via `.env`)

### Admin Access
To access admin dashboard:
1. Navigate to `/admin` route
2. Requires admin privileges (set `is_admin = True` in database)

---

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Posts
- `GET /api/posts` - Get feed posts
- `POST /api/posts` - Create new post (with hate speech analysis)
- `POST /api/posts/<id>/like` - Like post
- `POST /api/posts/<id>/unlike` - Unlike post
- `POST /api/posts/<id>/comments` - Add comment

### Users
- `GET /api/users` - Get all users (admin)
- `GET /api/users/<id>` - Get user details
- `GET /api/users/<id>/posts` - Get user's posts

### Moderation
- `POST /api/analyze` - Analyze text for hate speech
- `POST /api/users/<id>/warn` - Warn user (admin)
- `POST /api/users/<id>/suspend` - Suspend user (admin)
- `POST /api/users/<id>/unsuspend` - Unsuspend user (admin)
- `GET /api/violations` - Get all violations (admin)
- `GET /api/statistics` - Get platform statistics

---

## 🤖 ML Model Details

### Model Architecture
- **Type:** Ensemble Model
- **Components:**
  1. Logistic Regression
  2. Random Forest Classifier
  3. Multinomial Naive Bayes
- **Vectorization:** TF-IDF (max 5000 features)
- **Accuracy:** 87.5%

### Categories Detected
- Racism
- Sexism
- Toxicity
- Offensive language
- Threats
- Identity hate

### Training
```python
# Train the model
python ml_model/train_model.py
```

---

## ⚙️ Configuration

### Environment Variables (`.env`)
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///hate_speech_detector.db
MAX_WARNINGS=3
MODEL_PATH=ml_model/hate_speech_model.pkl
VECTORIZER_PATH=ml_model/vectorizer.pkl
```

---

## 🧪 Testing

### Test Backend API
```powershell
python test_system.py
```

### Test Hate Speech Detection
```python
from backend.models.detector import HateSpeechDetector

detector = HateSpeechDetector()
result = detector.predict("Your test text here")
print(result)
```

---

## 🎨 UI Screenshots

### Feed View
- Instagram-style post cards
- Like & comment functionality
- Real-time updates

### Profile Page
- User stats (posts, warnings, violations)
- Post grid
- Account status

### Admin Dashboard
- Statistics cards
- User management table
- Violations log

---

## 🔒 Security Features

- Password hashing (Werkzeug)
- Session management
- CORS protection
- Input validation
- SQL injection prevention (SQLAlchemy ORM)

---

## 📊 Database Schema

### Users Table
- `id` - Primary key
- `username` - Unique username
- `email` - Unique email
- `password_hash` - Hashed password
- `warnings` - Warning count
- `is_suspended` - Suspension status
- `is_admin` - Admin privileges
- `created_at` - Registration date

### Posts Table
- `id` - Primary key
- `user_id` - Foreign key to users
- `content` - Post text
- `image_url` - Image URL (optional)
- `likes_count` - Number of likes
- `hate_detected` - Boolean flag
- `hate_category` - Category if detected
- `created_at` - Creation timestamp

### Violations Table
- `id` - Primary key
- `user_id` - Foreign key to users
- `content` - Flagged content
- `category` - Hate category
- `hate_score` - Detection confidence
- `action_taken` - Warning/Suspension
- `created_at` - Timestamp

---

## 🐛 Troubleshooting

### Backend won't start
- ✅ Check Python version (3.13.8 required)
- ✅ Activate virtual environment
- ✅ Install dependencies: `pip install -r requirements.txt`
- ✅ Verify port 5000 is available

### React won't compile
- ✅ Check Node.js installation
- ✅ Run `npm install` in `frontend-react/`
- ✅ Verify port 3000 is available
- ✅ Clear npm cache: `npm cache clean --force`

### Model not loading
- ✅ Train model: `python ml_model/train_model.py`
- ✅ Check `.pkl` files exist
- ✅ Verify paths in `.env`

### Database errors
- ✅ Delete `hate_speech_detector.db` and restart
- ✅ Check SQLAlchemy version (2.0.44)
- ✅ Run migrations if needed

---

## 📈 Performance

- **API Response Time:** < 100ms (typical)
- **ML Prediction Time:** < 50ms
- **Frontend Load Time:** ~2s (development)
- **Database:** Optimized with indexes

---

## 🚧 Future Enhancements

- [ ] Image content moderation
- [ ] Multi-language support
- [ ] Real-time notifications (WebSockets)
- [ ] Improved ML model (BERT/RoBERTa)
- [ ] Mobile app (React Native)
- [ ] Export reports (PDF)
- [ ] Appeal system for suspensions
- [ ] Content filtering options

---

## 📄 License

MIT License - Feel free to use this project for learning and development.

---

## 👨‍💻 Developer Notes

### Adding New Hate Categories
Edit `backend/utils/preprocessing.py`:
```python
HATE_KEYWORDS = {
    'new_category': ['keyword1', 'keyword2']
}
```

### Customizing UI Theme
Edit `frontend-react/src/index.js`:
```javascript
const theme = createTheme({
  palette: {
    primary: { main: '#your-color' }
  }
});
```

### Changing Warning Limit
Edit `.env`:
```
MAX_WARNINGS=5  # Change to desired number
```

---

## 🙏 Acknowledgments

- Dataset: Various hate speech datasets
- ML Libraries: scikit-learn, NLTK, Transformers
- UI Framework: Material-UI
- Community: Open source contributors

---

## 📞 Support

For issues or questions:
1. Check `QUICK_START.md` for setup help
2. Review API documentation
3. Check browser console for errors
4. Verify backend logs

---

**Built with ❤️ using Flask, React, and AI**

🌐 **Backend:** http://localhost:5000  
🎨 **Frontend:** http://localhost:3000  
📊 **Admin:** http://localhost:3000/admin

---

*Stay safe, stay respectful! 🛡️*
