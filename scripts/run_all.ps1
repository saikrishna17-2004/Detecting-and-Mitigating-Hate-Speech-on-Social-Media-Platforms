param(
    [int]$FrontendPort = 3000,
    [int]$BackendPort = 5000
)

Write-Host ""
Write-Host "========================================"
Write-Host "  Hate Speech Detection - Full Stack"
Write-Host "========================================"
Write-Host ""

# Start backend
Write-Host "Starting Backend..." -ForegroundColor Yellow
$backendCmd = ". .\.venv\Scripts\Activate.ps1; python run_flask_dev.py"
Start-Process -FilePath powershell -ArgumentList @("-NoExit", "-Command", $backendCmd) -WindowStyle Normal
Start-Sleep -Seconds 5
Write-Host "[OK] Backend started on http://localhost:$BackendPort" -ForegroundColor Green

# Start frontend
Write-Host ""
Write-Host "Starting Frontend..." -ForegroundColor Yellow
$frontendCmd = "cd frontend-react; npm start"
Start-Process -FilePath powershell -ArgumentList @("-NoExit", "-Command", $frontendCmd) -WindowStyle Normal
Start-Sleep -Seconds 8

Write-Host ""
Write-Host "========================================"
Write-Host "  Both services are now running!"
Write-Host "========================================"
Write-Host "Frontend: http://localhost:$FrontendPort" -ForegroundColor Green
Write-Host "Backend:  http://localhost:$BackendPort" -ForegroundColor Green
Write-Host ""
Write-Host "Opening app in browser..." -ForegroundColor Cyan

Start-Sleep -Seconds 2
Start-Process "http://localhost:$FrontendPort"

Write-Host "[OK] App launched! Press Ctrl+C in other windows to stop." -ForegroundColor Green
Write-Host ""
