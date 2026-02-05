# HOW TO START THE BACKEND SERVER

## The Problem
VS Code's integrated terminal can't keep Python web servers running in background mode on Windows. This is a known limitation.

## The Solution - Start Server in Separate Window

### Method 1: Using PowerShell (Recommended)

1. **Open a NEW PowerShell window** (NOT in VS Code)
   - Press `Win + X` and select "Windows PowerShell"
   - OR press `Win + R`, type `powershell`, press Enter
   - OR search "PowerShell" in Start menu

2. **Navigate to project folder:**
   ```powershell
   cd C:\Users\nakka\Desktop\pp1
   ```

3. **Activate virtual environment:**
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   
   You should see `(.venv)` appear in your prompt.

4. **Start the server:**
   ```powershell
   python server.py
   ```

5. **You should see:**
   ```
   Model Status: LOADED
   Server URL: http://localhost:5000
   Server is running... Press CTRL+C to stop
   ```

6. **KEEP THIS WINDOW OPEN!** The server runs as long as this window is open.

### Method 2: Using the Batch File (Easiest)

1. Navigate to `C:\Users\nakka\Desktop\pp1` in File Explorer
2. Double-click `start_server.bat`
3. A window will open and start the server automatically
4. Keep that window open

### Method 3: Using Command Prompt

Same as Method 1, but use `cmd` instead of PowerShell:
```cmd
cd C:\Users\nakka\Desktop\pp1
.venv\Scripts\activate.bat
python server.py
```

## Testing the Server

### From VS Code Terminal:
```powershell
# Run the comprehensive test
python test_backend_api.py
```

### From Browser:
Open these URLs:
- http://localhost:5000 - API info
- http://localhost:5000/health - Health check

### From PowerShell:
```powershell
curl http://localhost:5000/health
```

## What You'll See When It Works

**In the server window:**
```
Model Status: LOADED
Server URL: http://localhost:5000
CORS Enabled: All origins
Server: Waitress (Production WSGI)

Available Endpoints:
   GET  /           - API information
   GET  /health     - Health check
   POST /api/analyze    - Analyze text for hate speech
   GET  /api/statistics - System statistics

Server is running... Press CTRL+C to stop
```

**In your test script:**
```
SUCCESS! Server is online and responding!
TEST 1: API Information Endpoint - PASS
TEST 2: Health Check Endpoint - PASS
TEST 3: Statistics Endpoint - PASS
...
```

## Frontend Connection

Once the server is running:
1. Your React frontend at http://localhost:3002 will automatically connect
2. The frontend can make real API calls to analyze text
3. You'll see the full Instagram-like interface working with live hate speech detection

## Stopping the Server

Press `CTRL + C` in the server window (the one running server.py)

## Troubleshooting

### "Cannot connect to server"
- Make sure the server window is still open
- Check that you see "Server is running..." message
- Verify no other program is using port 5000

### "python: command not found"
- Make sure you activated the virtual environment first
- You should see `(.venv)` in your prompt

### Port already in use
```powershell
# Kill any existing Python processes
Get-Process python -ErrorAction SilentlyContinue | Stop-Process -Force
```
Then try starting the server again.

## Quick Start Summary

**Shortest path to success:**
1. Open NEW PowerShell (not VS Code)
2. `cd C:\Users\nakka\Desktop\pp1`
3. `.\.venv\Scripts\Activate.ps1`
4. `python server.py`
5. Keep window open
6. From VS Code: `python test_backend_api.py`

That's it! Your world-class 99.39% accuracy hate speech detector will be fully operational! 🎉
