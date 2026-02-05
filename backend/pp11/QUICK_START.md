# Quick Start Guide - Instagram-like Social Media with Hate Speech Detection

## 🚀 Getting Started

### Start the Backend API

Open Terminal 1 (PowerShell):
```powershell
# Navigate to backend directory
cd backend\pp11

# Start Flask server
python app.py
```
✅ Backend will run on: **http://localhost:5000**

---

### Start the React Frontend

Open Terminal 2 (PowerShell):
```powershell
# Navigate to React frontend
cd frontend-react

# Start development server
npm start
```
✅ React app will automatically open on: **http://localhost:3000**

---

## 📱 Using the Application

### 1. Register an Account
- Open http://localhost:3000
- Click "Sign Up"
- Enter username, email, and password
- Click "Sign Up" button

### 2. Create Posts
- Type your caption
- Add image URL (optional)
- Click "Post"
- **Note:** Posts with hate speech will be flagged

### 3. Interact with Posts
- ❤️ Like posts
- 💬 Add comments
- View user profiles

### 4. Moderation System
- **1st Offense:** ⚠️ Warning
- **2nd Offense:** ⚠️ Second warning
- **3rd Offense:** 🚫 Account suspended

---

## 🎯 Key Features

### User Features
- ✅ User registration & login
- ✅ Create posts with images
- ✅ Like & comment on posts
- ✅ View user profiles
- ✅ Instagram-style feed

### Moderation Features
- ✅ Real-time hate speech detection
- ✅ Automatic warnings & suspensions
- ✅ Content categorization
- ✅ Violation tracking

### Admin Features (for admin users)
- ✅ User management dashboard
- ✅ Violation monitoring
- ✅ Statistics overview
- ✅ Manual warn/suspend/unsuspend

---

## 🧪 Testing Hate Speech Detection

Try posting these examples:

### ✅ Safe Content
```
"Beautiful sunset today!"
"Having a great day with friends"
"Just finished my workout 💪"
```

### ⚠️ Will be Flagged (Testing only)
```
"I hate everyone" (General hate)
"This is terrible" (Negative language)
```

**Note:** The model will detect and warn/suspend based on content severity.

---

## 🎨 UI Overview

### Main Feed
- Create new posts
- View all posts from users
- Like and comment

### Profile Page
- View user stats (posts, warnings, violations)
- See all user posts
- Account status

### Admin Dashboard (Admin only)
- Statistics cards (users, suspensions, violations, hate rate)
- User management table
- Violations log

---

## 🛠️ Troubleshooting

### Backend not starting?
- Make sure Python virtual environment is activated
- Check if port 5000 is available
- Ensure all dependencies are installed

### React app not loading?
- Check if backend is running first
- Ensure port 3000 is available
- Check browser console for errors

### Can't create posts?
- Make sure you're logged in
- Check network tab for API errors
- Verify backend is responding

---

## 📂 Project Structure

```
pp11/
├── backend/
│   ├── app.py              # Flask app
│   ├── database.py         # Database models
│   ├── routes/
│   │   └── api.py          # API endpoints
│   └── models/
│       └── detector.py     # ML model
├── frontend-react/
│   ├── src/
│   │   ├── App.js          # Main app
│   │   ├── components/     # React components
│   │   │   ├── auth/       # Login, Register
│   │   │   ├── posts/      # Feed, PostCard, CreatePost
│   │   │   ├── profile/    # Profile page
│   │   │   ├── admin/      # Admin dashboard
│   │   │   ├── layout/     # Navbar
│   │   │   └── moderation/ # Moderation alerts
│   │   └── services/
│   │       └── api.js      # API calls
│   └── package.json
└── ml_model/
    └── hate_speech_model.pkl  # Trained model
```

---

## 🔐 Default Admin Access

To create an admin user, you'll need to manually set `is_admin = True` in the database or create one via Python:

```python
from backend.database import db, User
from backend.app import create_app

app = create_app()
with app.app_context():
    user = User.query.filter_by(username='your_username').first()
    user.is_admin = True
    db.session.commit()
```

---

## 🎉 You're All Set!

Your Instagram-like social media platform with AI-powered hate speech detection is ready to use!

**Access Points:**
- 🌐 Frontend: http://localhost:3000
- 🔧 Backend API: http://localhost:5000
- 📊 API Health: http://localhost:5000/api/statistics

---

## 💡 Tips

1. **Create multiple accounts** to test social features
2. **Post various content** to see moderation in action
3. **Check admin dashboard** to monitor violations
4. **Test edge cases** with borderline content

Enjoy building a safer social media experience! 🚀
