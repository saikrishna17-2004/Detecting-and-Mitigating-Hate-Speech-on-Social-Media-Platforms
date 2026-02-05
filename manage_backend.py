#!/usr/bin/env python
"""
Backend Server Daemon
Runs the Flask backend as a background process with process management
"""

import subprocess
import sys
import os
import signal
import time
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent
PID_FILE = PROJECT_ROOT / "backend_server.pid"
LOG_FILE = PROJECT_ROOT / "backend_server.log"
PYTHON_EXE = PROJECT_ROOT / ".venv" / "Scripts" / "python.exe"
BACKEND_SCRIPT = PROJECT_ROOT / "backend" / "app.py"

def is_server_running():
    """Check if server is already running"""
    if not PID_FILE.exists():
        return False
    
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
        
        # Check if process exists (Windows)
        if sys.platform == 'win32':
            import ctypes
            kernel32 = ctypes.windll.kernel32
            PROCESS_QUERY_INFORMATION = 0x0400
            handle = kernel32.OpenProcess(PROCESS_QUERY_INFORMATION, 0, pid)
            if handle:
                kernel32.CloseHandle(handle)
                return True
        return False
    except:
        return False

def start_server():
    """Start the backend server"""
    if is_server_running():
        print("⚠️  Backend server is already running")
        with open(PID_FILE, 'r') as f:
            pid = f.read().strip()
        print(f"   Process ID: {pid}")
        return
    
    print("🚀 Starting Backend Server...")
    
    # Start server process
    with open(LOG_FILE, 'w') as log:
        if sys.platform == 'win32':
            # Windows: Use CREATE_NEW_PROCESS_GROUP to detach
            CREATE_NEW_PROCESS_GROUP = 0x00000200
            DETACHED_PROCESS = 0x00000008
            
            process = subprocess.Popen(
                [str(PYTHON_EXE), str(BACKEND_SCRIPT)],
                stdout=log,
                stderr=subprocess.STDOUT,
                creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
                cwd=str(PROJECT_ROOT)
            )
        else:
            # Unix-like systems
            process = subprocess.Popen(
                [str(PYTHON_EXE), str(BACKEND_SCRIPT)],
                stdout=log,
                stderr=subprocess.STDOUT,
                start_new_session=True,
                cwd=str(PROJECT_ROOT)
            )
    
    # Save PID
    with open(PID_FILE, 'w') as f:
        f.write(str(process.pid))
    
    print(f"✅ Backend server started!")
    print(f"   Process ID: {process.pid}")
    print(f"   API URL: http://localhost:5000")
    print(f"   Log file: {LOG_FILE}")

def stop_server():
    """Stop the backend server"""
    if not is_server_running():
        print("⚠️  Backend server is not running")
        if PID_FILE.exists():
            PID_FILE.unlink()
        return
    
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
        
        print(f"🛑 Stopping Backend Server (PID: {pid})...")
        
        if sys.platform == 'win32':
            # Windows
            subprocess.run(['taskkill', '/F', '/PID', str(pid)], 
                         capture_output=True)
        else:
            # Unix-like
            os.kill(pid, signal.SIGTERM)
        
        time.sleep(1)
        PID_FILE.unlink()
        print("✅ Backend server stopped!")
        
    except Exception as e:
        print(f"❌ Error stopping server: {e}")
        if PID_FILE.exists():
            PID_FILE.unlink()

def status_server():
    """Check server status"""
    if is_server_running():
        with open(PID_FILE, 'r') as f:
            pid = f.read().strip()
        print("✅ Backend server is RUNNING")
        print(f"   Process ID: {pid}")
        print(f"   API URL: http://localhost:5000")
        print(f"   Log file: {LOG_FILE}")
    else:
        print("❌ Backend server is NOT running")
        if PID_FILE.exists():
            PID_FILE.unlink()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python manage_backend.py start   - Start the server")
        print("  python manage_backend.py stop    - Stop the server")
        print("  python manage_backend.py status  - Check server status")
        print("  python manage_backend.py restart - Restart the server")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == 'start':
        start_server()
    elif command == 'stop':
        stop_server()
    elif command == 'status':
        status_server()
    elif command == 'restart':
        stop_server()
        time.sleep(2)
        start_server()
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)
