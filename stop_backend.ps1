# Stop Backend Server
# This script stops the backend server if it's running

Write-Host "`n🛑 Stopping Backend Server..." -ForegroundColor Cyan

# Find the backend process
$backendProcess = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*backend\app.py*"
}

if ($backendProcess) {
    Write-Host "Found backend server (PID: $($backendProcess.Id))" -ForegroundColor Yellow
    Stop-Process -Id $backendProcess.Id -Force
    Write-Host "✅ Backend server stopped successfully!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Backend server is not running" -ForegroundColor Yellow
}

Write-Host "`nPress any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
