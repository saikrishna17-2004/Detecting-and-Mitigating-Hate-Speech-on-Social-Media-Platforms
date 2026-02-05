<#
  Deprecated detached helper. Use start_server.bat instead.
  This script now delegates to start_server.bat.
#>
Write-Host "`nStarting Backend API Server (Detached Mode)..." -ForegroundColor Cyan
if (-not (Test-Path -Path "start_server.bat")) {
  Write-Host "start_server.bat not found. Please run server via server.py manually." -ForegroundColor Red
  exit 1
}
Start-Process -FilePath "start_server.bat"
Write-Host "A new PowerShell window should now be running the server." -ForegroundColor Green
