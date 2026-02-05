# Backend Server Management Guide

## Problem
When VS Code closes, the backend server stops because terminal processes are killed.

## Solutions

### 🎯 Option 1: PowerShell Detached Mode (Easiest)

Run the backend in a separate window that persists after VS Code closes:

```powershell
.\start_backend_detached.ps1
```

This will:
- ✅ Open a new PowerShell window
- ✅ Start the Flask server in that window
- ✅ Keep running even after VS Code closes
- ✅ Save logs to `backend_server.log`

**To check if it's running:**
```powershell
.\check_backend.ps1
```

**To stop the server:**
```powershell
.\stop_backend.ps1
```

---

### 🎯 Option 2: Double-Click Batch File (Windows)

Simply double-click the file:
```
start_backend.bat
```

This opens a command window with the backend server. Keep the window open.

---

### 🎯 Option 3: Python Process Manager (Advanced)

Use the Python script for full control:

**Start the server:**
```powershell
python manage_backend.py start
```

**Check status:**
```powershell
python manage_backend.py status
```

**Stop the server:**
```powershell
python manage_backend.py stop
```

**Restart the server:**
```powershell
python manage_backend.py restart
```

---

## Recommended Workflow

### For Development (with VS Code open):
1. Use the regular script: `.\start_backend.ps1`
2. Server runs in VS Code terminal
3. Easy to see logs and errors

### For Testing/Production (VS Code closed):
1. Use detached mode: `.\start_backend_detached.ps1`
2. Server runs independently
3. Check status anytime: `.\check_backend.ps1`
4. Stop when done: `.\stop_backend.ps1`

---

## Auto-Start on Windows Boot (Optional)

To make the backend start automatically when Windows starts:

1. Press `Win + R`, type `shell:startup`, press Enter
2. Create a shortcut to `start_backend_detached.ps1`
3. Server will auto-start on boot

---

## Troubleshooting

### Server won't start?
```powershell
# Check Python environment
C:/Users/nakka/Desktop/pp1/.venv/Scripts/python.exe --version

# Check if port 5000 is in use
netstat -ano | findstr :5000

# View server logs
Get-Content backend_server.log -Tail 20
```

### Kill stuck process:
```powershell
# Find process using port 5000
netstat -ano | findstr :5000

# Kill by PID (replace XXXX with actual PID)
Stop-Process -Id XXXX -Force
```

---

## Quick Reference

| Script | Purpose | Persists after VS Code closes? |
|--------|---------|-------------------------------|
| `start_backend.ps1` | Development (VS Code terminal) | ❌ No |
| `start_backend_detached.ps1` | Detached (separate window) | ✅ Yes |
| `start_backend.bat` | Double-click start | ✅ Yes |
| `manage_backend.py start` | Background process | ✅ Yes |
| `check_backend.ps1` | Check if running | - |
| `stop_backend.ps1` | Stop server | - |

---

## Summary

**Before closing VS Code, run:**
```powershell
.\start_backend_detached.ps1
```

**When you open VS Code again, check:**
```powershell
.\check_backend.ps1
```

The server will still be running! 🎉
