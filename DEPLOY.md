# 🚀 Quick Deploy Guide

Your hate speech detection platform is ready to deploy to the cloud!

## 📋 Pre-flight Check

Run this to verify everything is ready:

```powershell
.\scripts\check_deployment_ready.ps1
```

## 🎯 Deployment Options

### Option 1: Cloud Deployment (Recommended) ⭐

Deploy to **Render (Backend)** + **Netlify (Frontend)**

**Time**: ~15 minutes  
**Cost**: FREE  
**Difficulty**: Easy

**Follow the complete guide**: [DEPLOYMENT_WALKTHROUGH.md](DEPLOYMENT_WALKTHROUGH.md)

**Quick summary**:
1. Push code to GitHub
2. Deploy backend on Render.com
3. Deploy frontend on Netlify.com
4. Done!

---

## 📚 All Deployment Documentation

Choose the guide that fits your needs:

| Guide | Description | When to Use |
|-------|-------------|-------------|
| **[DEPLOYMENT_WALKTHROUGH.md](DEPLOYMENT_WALKTHROUGH.md)** ⭐ | Step-by-step cloud deployment | First-time deployment |
| [DEPLOY_NOW.md](DEPLOY_NOW.md) | Quick deployment checklist | You've deployed before |
| [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | Detailed deployment guide | Need in-depth information |
| [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) | Complete checklist | Verify all steps |
| [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) | Render-specific guide | Render deployment only |

---

## ⚡ Quick Start (Cloud Deployment)

### Prerequisites
- [ ] GitHub account
- [ ] Render.com account (sign up with GitHub)
- [ ] Netlify.com account (sign up with GitHub)
- [ ] Code pushed to GitHub

### Step 1: Prepare
```powershell
# Commit all changes
git add .
git commit -m "Ready for deployment"

# Push to GitHub
git push origin main
```

### Step 2: Deploy Backend (Render)
1. Go to https://render.com
2. New → Web Service
3. Connect your repository
4. Configure:
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn -w 4 -b 0.0.0.0:$PORT run_backend:app`
5. Add environment variables (from [DEPLOYMENT_WALKTHROUGH.md](DEPLOYMENT_WALKTHROUGH.md))
6. Deploy!

### Step 3: Deploy Frontend (Netlify)
1. Go to https://netlify.com
2. New site → Import from GitHub
3. Configure:
   - Base: `frontend-react`
   - Build: `npm run build`
   - Publish: `frontend-react/build`
4. Add env var: `REACT_APP_API_BASE_URL=https://your-backend.onrender.com/api`
5. Deploy!

### Step 4: Connect
Update backend `FRONTEND_URL` in Render to your Netlify URL.

---

## 🎉 After Deployment

Your app will be live at:
- **Backend**: `https://your-app.onrender.com`
- **Frontend**: `https://your-app.netlify.app`

Test it:
- ✅ Register account
- ✅ Login
- ✅ Create post
- ✅ Test hate speech detection

---

## 🐛 Troubleshooting

**Backend won't start?**
- Check Render logs
- Verify MongoDB Atlas allows 0.0.0.0/0

**Frontend can't connect?**
- Check `REACT_APP_API_BASE_URL` in Netlify
- Verify backend `FRONTEND_URL` is correct

**More help**: See troubleshooting section in [DEPLOYMENT_WALKTHROUGH.md](DEPLOYMENT_WALKTHROUGH.md)

---

## 📊 Project URLs (Update After Deployment)

| Service | URL | Status |
|---------|-----|--------|
| Backend API | `https://__________.onrender.com` | ⏳ Pending |
| Frontend App | `https://__________.netlify.app` | ⏳ Pending |
| GitHub Repo | https://github.com/saikrishna17-2004/Detecting-and-Mitigating-Hate-Speech-on-Social-Media-Platforms | ✅ Active |
| MongoDB Atlas | https://cloud.mongodb.com | ✅ Connected |

---

**Ready?** Start with the **[DEPLOYMENT_WALKTHROUGH.md](DEPLOYMENT_WALKTHROUGH.md)** guide! 🚀
