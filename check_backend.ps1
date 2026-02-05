# Check Backend Server Status
# This script checks if the backend server is running

Write-Host "`n🔍 Checking Backend Server Status..." -ForegroundColor Cyan

# Find the backend process
$backendProcess = Get-Process python -ErrorAction SilentlyContinue | Where-Object {
    $_.CommandLine -like "*backend\app.py*"
}

if ($backendProcess) {
    Write-Host "`n✅ Backend server is RUNNING" -ForegroundColor Green
    Write-Host "   Process ID: $($backendProcess.Id)" -ForegroundColor Cyan
    Write-Host "   API URL: http://localhost:5000" -ForegroundColor Green
    
    # Try to test the API
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:5000" -Method Get -TimeoutSec 2
        Write-Host "`n   API Response:" -ForegroundColor Yellow
        Write-Host "   Message: $($response.message)" -ForegroundColor White
        Write-Host "   Version: $($response.version)" -ForegroundColor White
    } catch {
        Write-Host "`n   ⚠️ Server process exists but API not responding" -ForegroundColor Yellow
    }
} else {
    Write-Host "`n❌ Backend server is NOT running" -ForegroundColor Red
    Write-Host "   Run .\start_backend_detached.ps1 to start it" -ForegroundColor Yellow
}

Write-Host "`nPress any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
