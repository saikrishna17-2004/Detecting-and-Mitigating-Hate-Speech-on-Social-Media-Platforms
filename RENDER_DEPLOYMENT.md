# Render Deployment Guide

## MongoDB Atlas Setup

1. Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster
3. Create a database user with username/password
4. Get your connection string: `mongodb+srv://username:password@cluster.mongodb.net/hate_speech_db?retryWrites=true&w=majority`

## Environment Variables on Render

Set these in your Render dashboard:

```
DATABASE_URL=mongodb+srv://username:password@cluster.mongodb.net/hate_speech_db?retryWrites=true&w=majority
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
PORT=10000
```

## Deployment Steps

1. Connect your GitHub repository to Render
2. Create a new Web Service
3. Select your repository
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn -w 4 -b 0.0.0.0:$PORT run_backend:app`
6. Add environment variables
7. Deploy!

## React Frontend (Netlify)

1. Build: `npm run build`
2. Publish directory: `build/`
3. Update API URL in `frontend-react/src/services/api.js` to your Render URL

## Health Check

Once deployed, test with:
```bash
curl https://your-render-url.com/health
```
