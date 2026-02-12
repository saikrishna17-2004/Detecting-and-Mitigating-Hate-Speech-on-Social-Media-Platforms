# 🚀 Deployment Walkthrough - Cloud Deployment

## ✅ Prerequisites Checklist

Run this before deploying:

```powershell
# 1. Check Git status
git status

# 2. Make sure everything is committed
git add .
git commit -m "Ready for cloud deployment"

# 3. Push to GitHub
git push origin main
```

---

## 🔧 Part 1: Deploy Backend to Render (5 minutes)

### Step 1: Create Render Account
1. Go to: **https://render.com**
2. Click **"Get Started"** or **"Sign In"**
3. Choose **"Sign up with GitHub"**
4. Authorize Render to access your repositories

### Step 2: Create Web Service
1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Find and select your repository:
   - **`Detecting-and-Mitigating-Hate-Speech-on-Social-Media-Platforms`**
4. Click **"Connect"**

### Step 3: Configure Service
Fill in these settings:

| Setting | Value |
|---------|-------|
| **Name** | `hate-speech-api` (or your choice) |
| **Region** | Choose closest to you (e.g., Oregon, Frankfurt) |
| **Branch** | `main` |
| **Root Directory** | Leave empty |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn -w 4 -b 0.0.0.0:$PORT run_backend:app` |
| **Instance Type** | **Free** |

### Step 4: Add Environment Variables
Scroll down to **"Environment Variables"** section and click **"Add Environment Variable"**.

Add these one by one:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `mongodb+srv://SAIKRISHNA:YadavNakkala@cluster0.osgwmcy.mongodb.net/hate_speech_db?retryWrites=true&w=majority` |
| `SECRET_KEY` | `ib90onHydhLh8cpoAUYLIyA0bAVQrKb7BVSYcRMISsg` |
| `JWT_SECRET_KEY` | `JJFEZ6Cvc1YhQ45nRsm2mMaqyPURX-sFrGMHfBohr9A` |
| `FLASK_ENV` | `production` |
| `FRONTEND_URL` | `*` (update this later with your Netlify URL) |

### Step 5: Create Service
1. Click **"Create Web Service"** button (bottom)
2. Wait for deployment (3-5 minutes)
   - Watch the build logs
   - Look for "Build successful" then "Live"
3. **Copy your Render URL**: `https://hate-speech-api-XXXX.onrender.com`

### Step 6: Test Backend
Open your Render URL in browser or test:
```powershell
curl https://your-render-url.onrender.com/health
```

Expected response:
```json
{"status": "healthy", "model_loaded": true}
```

✅ **Backend deployment complete!**

---

## 🎨 Part 2: Deploy Frontend to Netlify (5 minutes)

### Step 1: Create Netlify Account
1. Go to: **https://app.netlify.com**
2. Click **"Sign up"**
3. Choose **"GitHub"**
4. Authorize Netlify

### Step 2: Create New Site
1. Click **"Add new site"** button
2. Choose **"Import an existing project"**
3. Click **"GitHub"**
4. Search and select: **`Detecting-and-Mitigating-Hate-Speech-on-Social-Media-Platforms`**
5. Click on the repository

### Step 3: Configure Build Settings
Fill in these settings:

| Setting | Value |
|---------|-------|
| **Site name** | Choose a unique name (e.g., `hate-speech-detector-yourname`) |
| **Branch to deploy** | `main` |
| **Base directory** | `frontend-react` |
| **Build command** | `npm run build` |
| **Publish directory** | `frontend-react/build` |

### Step 4: Add Environment Variable
1. Click **"Show advanced"**
2. Click **"New variable"**
3. Add:
   - **Key**: `REACT_APP_API_BASE_URL`
   - **Value**: `https://your-render-url.onrender.com/api`
     (Use your actual Render URL from Part 1, Step 5)

### Step 5: Deploy Site
1. Click **"Deploy site"**
2. Wait for deployment (2-3 minutes)
   - Watch the build progress
   - Look for "Site is live"
3. **Copy your Netlify URL**: `https://your-site-name.netlify.app`

### Step 6: Test Frontend
1. Open your Netlify URL in browser
2. You should see the login/register page
3. Try creating an account and posting

✅ **Frontend deployment complete!**

---

## 🔄 Part 3: Update Backend CORS (2 minutes)

Now that both are deployed, update the backend to only allow your frontend:

### Step 1: Update Render Environment
1. Go back to **Render Dashboard**
2. Click on your **Web Service** (`hate-speech-api`)
3. Click **"Environment"** tab (left sidebar)
4. Find `FRONTEND_URL` variable
5. Click **"Edit"**
6. Change value to: `https://your-site-name.netlify.app`
   (Use your actual Netlify URL)
7. Click **"Save Changes"**

This will automatically trigger a redeploy (1-2 minutes).

✅ **CORS configuration complete!**

---

## ✨ You're Live!

Your project is now deployed:

- **Backend API**: `https://your-render-url.onrender.com`
- **Frontend App**: `https://your-site-name.netlify.app`

### Test Everything:
1. ✅ Register a new account
2. ✅ Login
3. ✅ Create a post
4. ✅ Test hate speech detection
5. ✅ Like/comment features
6. ✅ Check profile page

---

## 📊 Monitoring & Maintenance

### Render Dashboard
- View logs: Click on service → "Logs" tab
- Monitor usage: "Metrics" tab
- Redeploy: "Manual Deploy" → "Deploy latest commit"

### Netlify Dashboard
- View deploys: Click on site → "Deploys" tab
- Monitor analytics: "Analytics" tab
- Update environment: "Site configuration" → "Environment variables"

### MongoDB Atlas
- Monitor usage: Click cluster → "Metrics" tab
- View collections: "Browse Collections"
- Backup data: "Cloud Backup" tab

---

## 🐛 Common Issues

### Issue: "Application failed to respond"
**Solution**: Check Render logs for errors. Usually MongoDB connection issue.
- Verify MongoDB Atlas allows 0.0.0.0/0
- Check DATABASE_URL is correct

### Issue: Frontend shows network error
**Solution**: Check environment variable
- Verify `REACT_APP_API_BASE_URL` in Netlify
- Must end with `/api` not just the domain

### Issue: CORS errors in browser
**Solution**: Update backend FRONTEND_URL
- Must match your Netlify URL exactly
- Don't include trailing `/`

---

## 🔐 Security Reminder

After successful deployment:

1. ✅ Verify `.env` is in `.gitignore`
2. ✅ Never commit secrets to GitHub
3. ✅ Consider restricting MongoDB network access to Render IPs only
4. ✅ Regularly update dependencies

---

**Need help?** Check logs in Render/Netlify dashboards or refer to:
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)
