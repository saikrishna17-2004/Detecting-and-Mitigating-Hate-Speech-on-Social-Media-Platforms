# 🚀 DEPLOYMENT - QUICK REFERENCE

## ✅ Status: READY TO DEPLOY

### Files Created for You:
- ✅ **DEPLOY_NOW.md** - Start here! Quick deployment guide
- ✅ **DEPLOYMENT_CHECKLIST.md** - Detailed step-by-step
- ✅ **verify_deployment.ps1** - Run to check readiness
- ✅ **show_deployment_info.py** - Display deployment info

---

## 🎯 3-Step Deployment

### 1️⃣ Push to GitHub
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2️⃣ Deploy Backend (Render)
- Go to https://render.com
- New Web Service → Connect GitHub
- Add 5 environment variables (see below)

### 3️⃣ Deploy Frontend (Netlify)  
- Go to https://netlify.com
- New Site → Import from GitHub
- Set base directory: `frontend-react`
- Add env var: `REACT_APP_API_BASE_URL`

---

## 🔑 Environment Variables for Render

Copy-paste these into Render dashboard:

```
DATABASE_URL=mongodb+srv://SAIKRISHNA:YadavNakkala@cluster0.osgwmcy.mongodb.net/hate_speech_db?retryWrites=true&w=majority

SECRET_KEY=ib90onHydhLh8cpoAUYLIyA0bAVQrKb7BVSYcRMISsg

JWT_SECRET_KEY=JJFEZ6Cvc1YhQ45nRsm2mMaqyPURX-sFrGMHfBohr9A

FLASK_ENV=production

FRONTEND_URL=https://your-netlify-site.netlify.app
```

*(Update FRONTEND_URL after Netlify deployment)*

---

## 🛠️ Render Build Settings

| Setting | Value |
|---------|-------|
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn -w 4 -b 0.0.0.0:$PORT run_backend:app` |
| Instance Type | Free |

---

## 🎨 Netlify Build Settings

| Setting | Value |
|---------|-------|
| Base directory | `frontend-react` |
| Build command | `npm run build` |
| Publish directory | `frontend-react/build` |

**Environment Variable:**
- Key: `REACT_APP_API_BASE_URL`
- Value: `https://your-render-url.onrender.com/api`

---

## 📋 Verification Checklist

Run `.\verify_deployment.ps1` to check:
- [x] Git repository configured
- [x] All required files present
- [x] Gunicorn installed
- [x] PyMongo installed
- [x] MongoDB connection configured

---

## 🆘 Need Help?

1. **Quick Start**: Read `DEPLOY_NOW.md`
2. **Detailed Guide**: Read `DEPLOYMENT_CHECKLIST.md`
3. **Full Documentation**: Read `DEPLOYMENT_GUIDE.md`

---

## 🔗 Platform URLs

- **Render**: https://render.com
- **Netlify**: https://netlify.com  
- **MongoDB Atlas**: https://cloud.mongodb.com

---

**Your project is production-ready. Start deploying now!** 🎉
