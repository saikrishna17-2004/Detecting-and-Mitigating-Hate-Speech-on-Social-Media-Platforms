# 🚀 Step-by-Step Deployment Process

Follow these steps **in order**. Each step builds on the previous one.

---

## ✅ STEP 1: Prepare Your Code (5 minutes)

### 1.1 Commit All Changes
```powershell
git status
git add .
git commit -m "Ready for cloud deployment"
```

### 1.2 Push to GitHub
```powershell
git push origin main
```

### 1.3 Verify Push
- Go to: https://github.com/saikrishna17-2004/Detecting-and-Mitigating-Hate-Speech-on-Social-Media-Platforms
- Check that your latest commit appears
- ✅ **Checkpoint**: Code is on GitHub

---

## 🔧 STEP 2: Deploy Backend on Render (7 minutes)

### 2.1 Create Render Account
1. Open browser → https://render.com
2. Click **"Get Started"** (top right)
3. Click **"Sign up with GitHub"**
4. Authorize Render (allow repository access)
5. ✅ You're now logged into Render

### 2.2 Create New Web Service
1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. You'll see a list of your GitHub repositories
4. Find: **"Detecting-and-Mitigating-Hate-Speech-on-Social-Media-Platforms"**
5. Click **"Connect"** button next to it

### 2.3 Configure Service Settings

Fill in the form **exactly** as shown:

| Field | Value |
|-------|-------|
| **Name** | `hate-speech-api` |
| **Region** | Oregon (US West) or choose nearest |
| **Branch** | `main` |
| **Root Directory** | *Leave empty* |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn -w 4 -b 0.0.0.0:$PORT run_backend:app` |

Scroll down to **Instance Type**:
- Select **"Free"** (0.1 CPU, 512 MB RAM)

### 2.4 Add Environment Variables

Scroll down to **"Environment Variables"** section.

Click **"Add Environment Variable"** for each one:

**Variable 1:**
- Key: `DATABASE_URL`
- Value: `mongodb+srv://SAIKRISHNA:YadavNakkala@cluster0.osgwmcy.mongodb.net/hate_speech_db?retryWrites=true&w=majority`

**Variable 2:**
- Key: `SECRET_KEY`
- Value: `ib90onHydhLh8cpoAUYLIyA0bAVQrKb7BVSYcRMISsg`

**Variable 3:**
- Key: `JWT_SECRET_KEY`
- Value: `JJFEZ6Cvc1YhQ45nRsm2mMaqyPURX-sFrGMHfBohr9A`

**Variable 4:**
- Key: `FLASK_ENV`
- Value: `production`

**Variable 5:**
- Key: `FRONTEND_URL`
- Value: `*`
- *(We'll update this later with your Netlify URL)*

### 2.5 Deploy Backend
1. Scroll to bottom
2. Click **"Create Web Service"** button
3. Wait for build to complete (3-5 minutes)
   - You'll see logs scrolling
   - Look for: "Installing dependencies..." then "Starting server..."
4. Wait for status to show **"Live"** (green dot)

### 2.6 Copy Your Backend URL
1. At the top of the page, you'll see your URL
2. It looks like: `https://hate-speech-api-XXXX.onrender.com`
3. **Write this down** or copy to notepad
4. Example: `https://hate-speech-api-abc123.onrender.com`

### 2.7 Test Backend
1. Click on your URL to open it
2. You should see JSON response like:
   ```json
   {
     "status": "online",
     "message": "Hate Speech Detection API",
     "model_loaded": true
   }
   ```
3. ✅ **Checkpoint**: Backend is live!

---

## 🎨 STEP 3: Deploy Frontend on Netlify (7 minutes)

### 3.1 Create Netlify Account
1. Open new tab → https://app.netlify.com
2. Click **"Sign up"**
3. Choose **"GitHub"**
4. Authorize Netlify
5. ✅ You're now logged into Netlify

### 3.2 Create New Site
1. Click **"Add new site"** button (green button)
2. Select **"Import an existing project"**
3. Click **"Deploy with GitHub"**
4. You'll see your repositories
5. Search for: **"Detecting-and-Mitigating-Hate-Speech-on-Social-Media-Platforms"**
6. Click on it

### 3.3 Configure Build Settings

**Site Settings:**
- **Site name**: Choose a unique name (e.g., `hate-speech-detector-yourname`)
  - This will be your URL: `yourname.netlify.app`

**Build Settings:**

| Field | Value |
|-------|-------|
| **Branch to deploy** | `main` |
| **Base directory** | `frontend-react` |
| **Build command** | `npm run build` |
| **Publish directory** | `frontend-react/build` |

### 3.4 Add Environment Variable

**IMPORTANT**: Before clicking Deploy!

1. Click **"Show advanced"** button
2. Click **"New variable"** button
3. Add this variable:
   - **Key**: `REACT_APP_API_BASE_URL`
   - **Value**: `https://your-backend-url.onrender.com/api`
   - ⚠️ **Replace** with YOUR actual Render URL from Step 2.6
   - ⚠️ Make sure to add `/api` at the end!
   - Example: `https://hate-speech-api-abc123.onrender.com/api`

### 3.5 Deploy Frontend
1. Click **"Deploy [your-site-name]"** button
2. Wait for deployment (2-4 minutes)
   - You'll see build progress
   - Status will change from "Building" → "Published"
3. Wait for green checkmark: "Published"

### 3.6 Copy Your Frontend URL
1. At the top you'll see: **"Site is live ✨"**
2. Your URL is shown: `https://your-site-name.netlify.app`
3. **Write this down** or copy to notepad
4. Example: `https://hate-speech-detector-john.netlify.app`

### 3.7 Test Frontend
1. Click on your Netlify URL
2. You should see the Login/Register page
3. ✅ **Checkpoint**: Frontend is live!

---

## 🔄 STEP 4: Connect Frontend to Backend (3 minutes)

### 4.1 Update Backend CORS
Now we need to tell the backend to accept requests from your frontend.

1. Go back to **Render Dashboard** tab
2. Click on your web service: **"hate-speech-api"**
3. Click **"Environment"** in left sidebar
4. Find the `FRONTEND_URL` variable
5. Click the **Edit** (pencil) icon next to it
6. Change the value from `*` to your **Netlify URL**
   - Example: `https://hate-speech-detector-john.netlify.app`
   - ⚠️ **No trailing slash!**
7. Click **"Save Changes"**

### 4.2 Wait for Redeploy
- Render will automatically redeploy (1-2 minutes)
- Wait for status to show **"Live"** again
- ✅ **Checkpoint**: CORS configured!

---

## 🎉 STEP 5: Test Everything (5 minutes)

### 5.1 Open Your App
Go to your Netlify URL: `https://your-site-name.netlify.app`

### 5.2 Test Registration
1. Click **"Sign Up"** / **"Register"**
2. Fill in:
   - Username: `test_user`
   - Email: `test@example.com`
   - Password: `Test123!`
3. Click **"Register"**
4. ✅ Should redirect to feed/home

### 5.3 Test Post Creation
1. Click **"Create Post"** or **"+"** button
2. Write some text: `Hello world! This is my first post.`
3. Click **"Post"**
4. ✅ Should see your post in the feed

### 5.4 Test Hate Speech Detection
1. Create another post with offensive text
2. System should:
   - Detect hate speech
   - Show warning
   - Not post it (depending on your config)
3. ✅ Hate speech detection working!

### 5.5 Test Login
1. Logout
2. Login with same credentials
3. ✅ Should see your posts

---

## ✅ DEPLOYMENT COMPLETE!

Your project is now **LIVE** on the internet! 🎉

### Your URLs:
- **Frontend**: `https://your-site-name.netlify.app`
- **Backend API**: `https://hate-speech-api-xxxx.onrender.com`

### Share these URLs:
You can now share your frontend URL with anyone!

---

## 📊 Post-Deployment: Monitor Your App

### Render Dashboard
- **View logs**: Click service → "Logs" tab
- **Monitor metrics**: Click "Metrics" tab
- **Manual redeploy**: "Manual Deploy" → "Deploy latest commit"

### Netlify Dashboard
- **View deploys**: Click site → "Deploys" tab
- **See logs**: Click on a deploy → "Deploy log"
- **Update env vars**: "Site configuration" → "Environment variables"

### MongoDB Atlas
- **Monitor usage**: https://cloud.mongodb.com → Click cluster → "Metrics"
- **View data**: "Browse Collections"

---

## 🐛 Troubleshooting

### ❌ Issue: Frontend shows "Network Error" or "Cannot connect to API"

**Fix:**
1. Check Netlify environment variable:
   - Go to Netlify → Site configuration → Environment variables
   - Verify `REACT_APP_API_BASE_URL` ends with `/api`
   - Should be: `https://your-backend.onrender.com/api`
2. If wrong, fix it and click "Trigger deploy" → "Clear cache and deploy"

### ❌ Issue: Backend shows "Application failed to respond"

**Fix:**
1. Check Render logs:
   - Render → Your service → Logs tab
   - Look for errors (usually MongoDB connection)
2. Verify MongoDB allows connections:
   - https://cloud.mongodb.com
   - Network Access → Should have `0.0.0.0/0`
3. Check DATABASE_URL is correct in Render environment variables

### ❌ Issue: CORS error in browser console

**Fix:**
1. Open browser developer tools (F12) → Console
2. If you see CORS error:
   - Go to Render → Environment
   - Update `FRONTEND_URL` to exact Netlify URL
   - Must match exactly (no trailing `/`)

### ❌ Issue: "Failed to build" on Render or Netlify

**Fix:**
1. Check build logs for specific error
2. Common fixes:
   - Render: Verify `requirements.txt` exists in repo root
   - Netlify: Verify base directory is `frontend-react`
   - Both: Push latest code and retry

---

## 🔄 Making Updates

When you make changes to your code:

### Update Backend:
```powershell
git add .
git commit -m "Updated backend"
git push origin main
```
- Render will auto-deploy (if enabled) or click "Manual Deploy"

### Update Frontend:
```powershell
git add .
git commit -m "Updated frontend"
git push origin main
```
- Netlify will auto-deploy

---

## 📝 Important Notes

1. ✅ **Free tier limitations**:
   - Render: May sleep after 15 min of inactivity (first request slow)
   - Netlify: 100 GB bandwidth/month
   - MongoDB Atlas: 512 MB storage

2. ✅ **Keep secure**:
   - Never commit `.env` file to GitHub
   - Keep MongoDB password safe
   - Don't share SECRET_KEY or JWT_SECRET_KEY

3. ✅ **After initial testing**:
   - Consider restricting MongoDB network access to Render's IPs only
   - Update to stronger secret keys if needed

---

## 🎓 What You've Accomplished

- ✅ Deployed a full-stack ML application to the cloud
- ✅ Set up production database (MongoDB Atlas)
- ✅ Configured CI/CD (auto-deploy from GitHub)
- ✅ Implemented CORS and security headers
- ✅ Created a publicly accessible web application

**Congratulations!** 🎊

---

Need help? Review the logs in Render/Netlify dashboards or check the detailed guides:
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- [DEPLOYMENT_WALKTHROUGH.md](DEPLOYMENT_WALKTHROUGH.md)
