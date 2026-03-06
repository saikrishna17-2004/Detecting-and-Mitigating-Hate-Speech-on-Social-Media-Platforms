# Check Backend Server Status
# This script checks if the backend server is listening on port 5000

Write-Host "`nChecking Backend Server Status..." -ForegroundColor Cyan

$listener = Get-NetTCPConnection -LocalPort 5000 -State Listen -ErrorAction SilentlyContinue |
    Select-Object -First 1

if ($listener) {
    $process = Get-Process -Id $listener.OwningProcess -ErrorAction SilentlyContinue
    Write-Host "`nBackend server is RUNNING" -ForegroundColor Green
    Write-Host "   Process ID: $($listener.OwningProcess)" -ForegroundColor Cyan
    if ($process) {
        Write-Host "   Process Name: $($process.ProcessName)" -ForegroundColor Cyan
    }
    Write-Host "   Listening On: $($listener.LocalAddress):$($listener.LocalPort)" -ForegroundColor Cyan
    Write-Host "   API URL: http://localhost:5000" -ForegroundColor Green
} else {
    Write-Host "`nBackend server is NOT running" -ForegroundColor Red
    Write-Host "   Run .\start_backend_detached.ps1 to start it" -ForegroundColor Yellow
    exit 1
}
