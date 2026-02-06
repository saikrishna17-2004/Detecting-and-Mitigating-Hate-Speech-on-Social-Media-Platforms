# 🚀 Deployment Checklist - Hate Speech Detection Platform

## ✅ Pre-Deployment Verification

Your project is **READY** for deployment! Here's what you need to do:

---

## 📊 Part 1: MongoDB Atlas Setup (Database)

### Step 1: Verify Your MongoDB Connection
You already have: `mongodb+srv://SAIKRISHNA:YadavNakkala@cluster0.osgwmcy.mongodb.net/?appName=Cluster0`

1. **Log in to MongoDB Atlas**: https://cloud.mongodb.com
2. **Navigate to Network Access**:
   - Click "Network Access" in left sidebar
   - Ensure **0.0.0.0/0** (Allow from anywhere) is added
   - If not, click "Add IP Address" → "Allow Access from Anywhere"

3. **Verify Database User**:
   - Click "Database Access"
   - Ensure user `SAIKRISHNA` exists with "Read and write to any database" permission

4. **Get Your Connection String**:
   ```
   mongodb+srv://SAIKRISHNA:YadavNakkala@cluster0.osgwmcy.mongodb.net/hate_speech_db?retryWrites=true&w=majority
   ```
   ⚠️ Note: I added `/hate_speech_db` as the database name

---

## 🔧 Part 2: Deploy Backend to Render

### Step 1: Push Code to GitHub
```powershell
# Make sure all changes are committed
git add .
git commit -m "Prepare for deployment"
git push origin main
```

### Step 2: Deploy on Render
1. **Go to**: https://render.com
2. **Sign up/Login** with GitHub
3. Click **"New +"** → **"Web Service"**
4. **Connect Repository**: 
   - Select: `saikrishna17-2004/Detecting-and-Mitigating-Hate-Speech-on-Social-Media-Platforms`
5. **Configure Service**:
   ```
   Name: hate-speech-api
   Region: Oregon (US West) or closest to you
   Branch: main
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn -w 4 -b 0.0.0.0:$PORT run_backend:app
   Instance Type: Free
   ```

### Step 3: Add Environment Variables
Click **"Environment"** tab and add these variables:

```bash
DATABASE_URL=mongodb+srv://SAIKRISHNA:YadavNakkala@cluster0.osgwmcy.mongodb.net/hate_speech_db?retryWrites=true&w=majority
FLASK_ENV=production
SECRET_KEY=your-secret-key-here-generate-new-one
JWT_SECRET_KEY=your-jwt-secret-here-generate-new-one
FRONTEND_URL=https://your-app-name.netlify.app
```

**Generate Secure Keys** (run locally in PowerShell):
```powershell
python -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"
```

### Step 4: Deploy
1. Click **"Create Web Service"**
2. Wait 3-5 minutes for build
3. Your API will be at: `https://hate-speech-api.onrender.com` (or your chosen name)
4. Test it: Open `https://your-render-url.onrender.com/health`

---

## 🎨 Part 3: Deploy Frontend to Netlify

### Step 1: Build React App Locally (Optional - to verify)
```powershell
cd frontend-react
npm install
npm run build
```

### Step 2: Deploy on Netlify
1. **Go to**: https://app.netlify.com
2. **Sign up/Login** with GitHub
3. Click **"Add new site"** → **"Import an existing project"**
4. **Connect to GitHub**:
   - Select: `saikrishna17-2004/Detecting-and-Mitigating-Hate-Speech-on-Social-Media-Platforms`
5. **Configure Build Settings**:
   ```
   Base directory: frontend-react
   Build command: npm run build
   Publish directory: frontend-react/build
   ```

### Step 3: Add Environment Variables
Click **"Site settings"** → **"Environment variables"** → **"Add a variable"**

```bash
REACT_APP_API_BASE_URL=https://your-render-url.onrender.com/api
```
Replace `your-render-url` with your actual Render URL from Part 2

### Step 4: Deploy
1. Click **"Deploy site"**
2. Wait 2-3 minutes
3. Your app will be at: `https://random-name-123.netlify.app`
4. Click **"Site settings"** → **"Change site name"** to customize

### Step 5: Update Backend FRONTEND_URL
1. Go back to **Render Dashboard**
2. Click your web service
3. Go to **"Environment"**
4. Update `FRONTEND_URL` to your Netlify URL: `https://your-site-name.netlify.app`
5. Click **"Save Changes"** (this will redeploy)

---

## 🧪 Part 4: Test Deployment

### Test Backend API
```powershell
# Health check
curl https://your-render-url.onrender.com/health

# Test registration
Invoke-WebRequest -Uri "https://your-render-url.onrender.com/api/auth/register" -Method POST -Body '{"username":"testuser","email":"test@example.com","password":"Test123!"}' -ContentType "application/json"
```

### Test Frontend
1. Open: `https://your-netlify-site.netlify.app`
2. Click "Register" and create an account
3. Login with your credentials
4. Try creating a post
5. Verify moderation alerts appear

---

## 📋 Post-Deployment Checklist

- [ ] MongoDB Atlas allows connections from anywhere (0.0.0.0/0)
- [ ] Backend deployed on Render and shows "Healthy" status
- [ ] Backend `/health` endpoint returns 200 OK
- [ ] Frontend deployed on Netlify
- [ ] Frontend can connect to backend API
- [ ] User registration works
- [ ] User login works
- [ ] Posts can be created and displayed
- [ ] Hate speech detection is working
- [ ] Admin dashboard is accessible

---

## 🔍 Troubleshooting

### Backend Issues
**Problem**: Build fails on Render
- Check build logs in Render dashboard
- Verify `requirements.txt` has all dependencies
- Ensure Python version is 3.10+ in Render settings

**Problem**: Backend crashes after deployment
- Check logs in Render dashboard
- Verify `DATABASE_URL` is correct
- Test MongoDB connection from Atlas dashboard

### Frontend Issues
**Problem**: Can't connect to backend
- Verify `REACT_APP_API_BASE_URL` in Netlify environment variables
- Check CORS settings in backend
- Ensure `FRONTEND_URL` in Render matches your Netlify URL

**Problem**: Build fails on Netlify
- Check build logs
- Verify `base directory: frontend-react`
- Ensure `package.json` exists in `frontend-react/`

### Database Issues
**Problem**: MongoDB connection timeout
- Add 0.0.0.0/0 to Network Access in MongoDB Atlas
- Verify connection string has correct password
- Check database user permissions

---

## 🎉 Success Indicators

When deployment is successful:
1. ✅ Backend URL shows API documentation at root
2. ✅ Frontend loads without errors
3. ✅ You can register and login
4. ✅ Posts appear in feed
5. ✅ Hate speech gets flagged with warnings

---

## 📞 Support Resources

- **Render Documentation**: https://render.com/docs
- **Netlify Documentation**: https://docs.netlify.com
- **MongoDB Atlas**: https://docs.atlas.mongodb.com

---

## 🔐 Security Reminders

1. ✅ Never commit `.env` file to GitHub
2. ✅ Use strong SECRET_KEY and JWT_SECRET_KEY
3. ✅ Keep MongoDB password secure
4. ✅ Update CORS settings to allow only your frontend URL in production
5. ✅ Enable MongoDB Atlas IP whitelist for specific IPs in production (currently set to 0.0.0.0/0 for testing)

---

**Your deployment is ready to start! Follow the steps above.**
