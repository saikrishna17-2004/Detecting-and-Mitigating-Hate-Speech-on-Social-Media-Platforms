<#
    Deprecated helper. Please use start_server.bat which opens a
    separate PowerShell window and runs the ASCII-safe production server.
    This script now delegates to start_server.bat for reliability.
#>
Write-Host "`nStarting Backend API Server..." -ForegroundColor Cyan
Write-Host "Using start_server.bat (recommended)" -ForegroundColor Yellow
Write-Host "API will be available at: http://localhost:5000`n" -ForegroundColor Green

# Full path to Python executable
$pythonExe = "C:/Users/nakka/Desktop/pp1/.venv/Scripts/python.exe"

if (-not (Test-Path -Path "start_server.bat")) {
  Write-Host "start_server.bat not found. Please run server via server.py manually." -ForegroundColor Red
  exit 1
}

# Delegate to batch launcher
Start-Process -FilePath "start_server.bat"
Write-Host "A new PowerShell window should now be running the server." -ForegroundColor Green
