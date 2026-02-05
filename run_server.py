"""
Backend Server Launcher with Keep-Alive
This script ensures the server stays running
"""
import sys
import subprocess
import time
from pathlib import Path

project_root = Path(__file__).parent
python_exe = project_root / ".venv" / "Scripts" / "python.exe"
server_script = project_root / "production_backend.py"

print("\n" + "="*70)
print("BACKEND SERVER LAUNCHER")
print("="*70)
print(f"\nPython: {python_exe}")
print(f"Script: {server_script}")
print("\nStarting server...")
print("="*70 + "\n")

try:
    # Run the server as a subprocess, keeping this process alive
    process = subprocess.Popen(
        [str(python_exe), str(server_script)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        universal_newlines=True
    )
    
    # Stream output
    print("Server process started. Streaming output...\n")
    
    for line in process.stdout:
        print(line, end='')
        sys.stdout.flush()
    
    process.wait()
    
except KeyboardInterrupt:
    print("\n\nStopping server...")
    if process:
        process.terminate()
        process.wait()
    print("Server stopped")
    
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()
