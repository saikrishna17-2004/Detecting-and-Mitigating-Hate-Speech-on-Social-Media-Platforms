# 🎯 Quick Start - Deploy Your Project

## ✅ Your Project is READY TO DEPLOY!

All checks passed! Follow these simple steps:

---

## 📦 Part 1: Deploy Backend (Render)

### Step 1: Push to GitHub
```powershell
git add .
git commit -m "Ready for deployment"
git push origin main
```

### Step 2: Deploy on Render
1. Go to: **https://render.com**
2. Click **"Sign up with GitHub"** or **"Login"**
3. Click **"New +"** → **"Web Service"**
4. Select repository: **`Detecting-and-Mitigating-Hate-Speech-on-Social-Media-Platforms`**
5. Configure:
   - **Name**: `hate-speech-api` (or your choice)
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT run_backend:app`
   - **Instance Type**: `Free`

### Step 3: Add Environment Variables
Click **"Environment"** tab and add these (one by one):

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `mongodb+srv://SAIKRISHNA:YadavNakkala@cluster0.osgwmcy.mongodb.net/hate_speech_db?retryWrites=true&w=majority` |
| `SECRET_KEY` | `ib90onHydhLh8cpoAUYLIyA0bAVQrKb7BVSYcRMISsg` |
| `JWT_SECRET_KEY` | `JJFEZ6Cvc1YhQ45nRsm2mMaqyPURX-sFrGMHfBohr9A` |
| `FLASK_ENV` | `production` |
| `FRONTEND_URL` | `https://your-site.netlify.app` (update after Step 6) |

### Step 4: Deploy
- Click **"Create Web Service"**
- Wait 3-5 minutes
- Your backend will be at: `https://hate-speech-api.onrender.com`

### Step 5: Test Backend
Click on your service URL or test:
```powershell
curl https://your-render-url.onrender.com/health
```

---

## 🎨 Part 2: Deploy Frontend (Netlify)

### Step 6: Deploy on Netlify
1. Go to: **https://app.netlify.com**
2. Click **"Sign up with GitHub"** or **"Login"**
3. Click **"Add new site"** → **"Import an existing project"**
4. Choose **"GitHub"**
5. Select repository: **`Detecting-and-Mitigating-Hate-Speech-on-Social-Media-Platforms`**
6. Configure build settings:
   - **Base directory**: `frontend-react`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend-react/build`

### Step 7: Add Environment Variable
1. Before deploying, click **"Site configuration"**
2. Go to **"Environment variables"**
3. Click **"Add a variable"**
   - **Key**: `REACT_APP_API_BASE_URL`
   - **Value**: `https://your-render-url.onrender.com/api` (use your Render URL from Step 4)
4. Click **"Deploy site"**
5. Wait 2-3 minutes

### Step 8: Update Backend FRONTEND_URL
1. Go back to **Render Dashboard**
2. Click on your web service
3. Go to **"Environment"** tab
4. Update `FRONTEND_URL` to: `https://your-site-name.netlify.app`
5. Save (this will trigger a redeploy)

### Step 9: Test Frontend
1. Open your Netlify URL
2. Try:
   - Register a new account
   - Login
   - Create a post
   - Test hate speech detection

---

## 🎉 You're Done!

Your hate speech detection platform is now live!

**Backend API**: `https://your-render-url.onrender.com`  
**Frontend App**: `https://your-netlify-site.netlify.app`

---

## 📋 Troubleshooting

### Backend won't start on Render?
- Check logs in Render dashboard
- Verify environment variables are set correctly
- Ensure MongoDB Atlas allows connections from anywhere (0.0.0.0/0)

### Frontend can't connect to backend?
- Check `REACT_APP_API_BASE_URL` in Netlify environment variables
- Verify `FRONTEND_URL` in Render matches your Netlify URL
- Check browser console for CORS errors

### Database connection errors?
1. Go to **MongoDB Atlas** (https://cloud.mongodb.com)
2. Click **"Network Access"**
3. Add **0.0.0.0/0** (Allow from anywhere)
4. Verify database user exists with correct password

---

## 📚 More Information

For detailed instructions, see:
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Complete step-by-step guide
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Original deployment documentation
- [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) - Render-specific guide

---

## 🔒 Important Security Notes

1. ✅ Never commit `.env` to GitHub (already in `.gitignore`)
2. ✅ Keep your MongoDB password secure
3. ✅ Change SECRET_KEY and JWT_SECRET_KEY for production (use the ones above)
4. ⚠️ After testing, restrict MongoDB Network Access to specific IPs for better security

---

**Need help?** Check the troubleshooting section above or review the detailed documentation files.
