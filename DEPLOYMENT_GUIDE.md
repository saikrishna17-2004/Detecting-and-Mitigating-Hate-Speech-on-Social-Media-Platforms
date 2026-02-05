# 🚀 Deployment Guide: Render + MongoDB Atlas

## Step 1: MongoDB Atlas Setup

### Create MongoDB Cluster
1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Sign up or log in
3. Create a new project called "Hate Speech Detection"
4. Create a free cluster (M0 tier is free)
5. Wait for cluster to be created (~5 minutes)

### Create Database User
1. Go to **Database Access** → **Add New Database User**
2. Enter username: `hate_user`
3. Enter password: Generate a secure password (copy it!)
4. Set permissions: **Read and write to any database**
5. Click **Add User**

### Get Connection String
1. Go to **Database** → Click **Connect** on your cluster
2. Choose **Drivers**
3. Copy the connection string:
   ```
   mongodb+srv://hate_user:PASSWORD@cluster.mongodb.net/?retryWrites=true&w=majority
   ```
4. Replace `PASSWORD` with your actual password
5. Add database name: 
   ```
   mongodb+srv://hate_user:PASSWORD@cluster.mongodb.net/hate_speech_db?retryWrites=true&w=majority
   ```

### Allow Network Access
1. Go to **Network Access**
2. Click **Add IP Address**
3. Select **Allow Access from Anywhere** (0.0.0.0/0)
4. Click **Confirm**

---

## Step 2: Render Deployment

### Connect GitHub Repository
1. Go to [Render.com](https://render.com)
2. Sign up with GitHub (authorize Render)
3. Go to **Dashboard**
4. Click **Create +** → **Web Service**
5. Select your GitHub repository
6. Fill in service details:
   - **Name**: `hate-speech-api`
   - **Region**: `us-east` (or nearest to you)
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT run_backend:app`
   - **Instance Type**: Free (for testing)

### Add Environment Variables
Click **Environment** and add:

```
DATABASE_URL=mongodb+srv://hate_user:YOUR_PASSWORD@cluster.mongodb.net/hate_speech_db?retryWrites=true&w=majority
SECRET_KEY=generate-a-random-secret-key-here
JWT_SECRET_KEY=generate-another-random-secret-key-here
FLASK_ENV=production
FRONTEND_URL=https://your-frontend-url.netlify.app
```

### Generate Secure Keys
Use this command to generate keys:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Run it twice and paste the values.

### Deploy
1. Click **Create Web Service**
2. Wait for deployment (2-5 minutes)
3. Your API will be at: `https://hate-speech-api.onrender.com`

---

## Step 3: React Frontend (Netlify)

### Build Frontend
```bash
cd frontend-react
npm run build
```

### Deploy to Netlify
1. Go to [Netlify.com](https://netlify.com)
2. Sign up with GitHub
3. Click **New site from Git**
4. Connect GitHub repository
5. Build settings:
   - **Base directory**: `frontend-react`
   - **Build command**: `npm run build`
   - **Publish directory**: `frontend-react/build`

### Update API URL
Edit `frontend-react/src/services/api.js`:
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'https://hate-speech-api.onrender.com/api';
```

Add environment variable in Netlify:
```
REACT_APP_API_URL=https://hate-speech-api.onrender.com/api
```

---

## Step 4: Verification

### Test Backend
```bash
curl https://hate-speech-api.onrender.com/
curl https://hate-speech-api.onrender.com/api/posts
```

### Test Frontend
Visit your Netlify domain, should load without errors.

---

## Monitoring & Troubleshooting

### View Render Logs
1. Go to your service on Render
2. Click **Logs** tab
3. Check for errors

### Common Issues

**Issue**: `ModuleNotFoundError`
- **Solution**: Check `requirements.txt` is committed to git

**Issue**: `DATABASE_URL` error
- **Solution**: Verify MongoDB connection string and IP whitelist

**Issue**: CORS errors
- **Solution**: Update `FRONTEND_URL` in Render environment variables

---

## Cost Breakdown (Free Tier)

- **Render Web Service**: Free (with limitations)
- **MongoDB Atlas M0**: Free forever
- **Netlify**: Free for static sites
- **Total**: $0/month for small projects

---

## Production Best Practices

1. **Use strong database credentials**
2. **Enable MongoDB IP whitelisting in production**
3. **Set up SSL/TLS certificates (automatic on Render)**
4. **Monitor API logs regularly**
5. **Set up error tracking (Sentry integration)**
6. **Regular database backups**

---

## Next Steps

1. Commit these changes to GitHub
2. Follow steps above to deploy
3. Test both backend and frontend
4. Monitor logs for any issues
5. Consider upgrading to paid tier for production use
