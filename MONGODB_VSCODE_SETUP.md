# MongoDB Atlas Connection Setup in VS Code

## Connection String
```
mongodb+srv://SAIKRISHNA:YadavNakkala@cluster0.osgwmcy.mongodb.net/hate_speech_db?retryWrites=true&w=majority
```

## Steps to Connect in VS Code

### 1. Open MongoDB Extension
- Click the **MongoDB icon** in the left sidebar (looks like a leaf)
- Or use `Ctrl+Shift+P` → Search "MongoDB: Open Overview"

### 2. Add Connection
- Click **"Add Connection"** or the **"+"** button
- Choose **"Connect with Connection String"**
- Paste the connection string above
- Name it: `Cluster0` (or any name you prefer)

### 3. Connection String Breakdown
```
mongodb+srv://           # Atlas connection protocol
SAIKRISHNA:              # Username
YadavNakkala@            # Password
cluster0.osgwmcy         # Cluster name
.mongodb.net/            # MongoDB Atlas domain
hate_speech_db           # Database name
?retryWrites=true        # Connection parameters
&w=majority              # Write concern
```

### 4. Verify Connection
Once connected, you should see in the MongoDB sidebar:
- ✅ **Cluster0** (connection name)
  - 📁 **hate_speech_db** (database)
    - 📊 **users** (collection)
    - 📊 **posts** (collection)
    - 📊 **violations** (collection)
    - 📊 **counters** (collection)

## If Connection Fails

### Error: "SSL handshake failed"
This means the MongoDB cluster is either:
1. **Paused** - Go to https://cloud.mongodb.com → Database → Cluster0 → Click **Resume**
2. **IP not whitelisted** - Go to Security → Network Access → Add **0.0.0.0/0** (Allow Access from Anywhere)

Wait 1-2 minutes for changes to apply.

## Using MongoDB Playground in VS Code

Once connected, you can:

### 1. Create a Playground
- Right-click **Cluster0** → Select **Create Playground**
- Or use `Ctrl+Shift+P` → "MongoDB: Create MongoDB Playground"

### 2. Write Queries
```javascript
// Find all users
db.users.find({});

// Find posts by a specific user
db.posts.find({user_id: 1});

// Count violations
db.violations.countDocuments();

// List all collections
db.listCollections();
```

### 3. Execute Query
- Click ▶️ **Run All** or `Ctrl+Shift+Enter`
- Results appear in a new panel

## Database Schema Reference

### Users Collection
```javascript
{
  _id: Number,
  username: String,
  email: String,
  password_hash: String,
  created_at: ISODate,
  warning_count: Number,
  is_suspended: Boolean,
  suspension_reason: String
}
```

### Posts Collection
```javascript
{
  _id: Number,
  user_id: Number,
  content: String,
  image_url: String,
  created_at: ISODate,
  likes_count: Number,
  comments: [
    {
      user_id: Number,
      content: String,
      created_at: ISODate
    }
  ]
}
```

### Violations Collection
```javascript
{
  _id: Number,
  user_id: Number,
  post_id: Number,
  violation_text: String,
  category: String,
  severity: String,
  action: String (warning|suspension),
  created_at: ISODate
}
```

### Counters Collection
```javascript
{
  _id: String,
  sequence_value: Number
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Authentication failed" | Check username/password in connection string |
| "Network timeout" | Cluster paused or IP not whitelisted |
| "Cannot connect" | Verify `.env` file has correct CONNECTION_URL |
| "Collection not found" | Run `init_db()` in Python to create collections |

## Testing via Python

If MongoDB extension doesn't work immediately, test from Python:

```powershell
python test_mongodb_connection.py
```

Expected output:
```
✅ Successfully connected to MongoDB Atlas!
Database: hate_speech_db
Collections: ['users', 'posts', 'violations', 'counters']
```

## Next Steps

1. ✅ Verify MongoDB extension is installed (`mongodb.mongodb-vscode`)
2. ✅ Add connection string in VS Code MongoDB panel
3. ⏳ Ensure MongoDB cluster is **RUNNING** (not paused)
4. ⏳ Ensure Network Access allows your IP
5. ✅ Browse databases/collections in VS Code
6. ✅ Create playgrounds to test queries
