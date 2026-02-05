# MongoDB Atlas Connection Setup

## Your MongoDB Connection Details

**Cluster**: cluster0.osgwmcy.mongodb.net  
**Username**: SAIKRISHNA  
**Connection String Template**: 
```
mongodb+srv://SAIKRISHNA:<db_password>@cluster0.osgwmcy.mongodb.net/hate_speech_db?retryWrites=true&w=majority
```

## Steps to Connect

### 1. Get Your MongoDB Password
1. Log in to [MongoDB Atlas](https://cloud.mongodb.com)
2. Go to **Database Access**
3. Find user `SAIKRISHNA`
4. Click **Edit** → **Show Password** (or reset if forgotten)
5. Copy your password

### 2. Update .env File
Replace `<db_password>` with your actual password in `.env`:

```env
DATABASE_URL=mongodb+srv://SAIKRISHNA:YOUR_ACTUAL_PASSWORD@cluster0.osgwmcy.mongodb.net/hate_speech_db?retryWrites=true&w=majority
```

**Example** (NOT real credentials):
```env
DATABASE_URL=mongodb+srv://SAIKRISHNA:myPassword123!@cluster0.osgwmcy.mongodb.net/hate_speech_db?retryWrites=true&w=majority
```

### 3. Verify Network Access
1. In MongoDB Atlas, go to **Network Access**
2. Ensure your IP is whitelisted or use **0.0.0.0/0** for development
3. Your IP should show: Allow access from anywhere (0.0.0.0/0)

### 4. Test Connection
Run this command to verify:
```bash
python test_mongodb_connection.py
```

Expected output:
```
✅ Successfully connected to MongoDB Atlas!
   Server version: X.X.X
   Available databases: [...]
   Current database: hate_speech_db
```

### 5. Verify Cluster Status
1. Go to MongoDB Atlas **Clusters**
2. Confirm cluster0 shows "RUNNING" status (not paused)
3. If paused, click **Resume**

## Common Issues

### SSL Certificate Error
- Ensure you're using the correct cluster URL
- Check that Python version is 3.7+ (you have 3.13.8 ✅)
- Update certifi: `pip install --upgrade certifi`

### Authentication Failed
- Verify username and password are correct
- Check that special characters in password are URL-encoded
- Reset password in MongoDB Atlas if needed

### Cannot Connect
- Ensure cluster is RUNNING (not paused)
- Add your current IP to Network Access: 0.0.0.0/0
- Check internet connection

## Next Steps

1. Update `.env` with your actual password
2. Run `python test_mongodb_connection.py` to verify
3. Commit changes: `git add . && git commit -m "Update MongoDB connection"`
4. Push to GitHub: `git push`
5. Run the application: the Flask app will use MongoDB automatically
