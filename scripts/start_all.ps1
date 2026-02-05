# Start backend and frontend in new windows (Windows PowerShell)
# Usage: .\scripts\start_all.ps1

param(
    [int]$FrontendPort = 3000
)

# Start backend (new window)
Write-Host "Starting backend in a new PowerShell window..."
$proj = (Get-Location).Path
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$proj'; .\.venv\Scripts\Activate.ps1; `$env:RUN_BACKEND_DIRECT='1'; python run_backend.py" -WorkingDirectory $proj

# Start frontend (new window)
if (Test-Path frontend-react\package.json) {
    Write-Host "Starting frontend (npm start) in a new PowerShell window..."
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$proj\frontend-react'; npm start" -WorkingDirectory "$proj\frontend-react"
} else {
    Write-Host "frontend-react not present; skipping frontend start."
}

Write-Host "Both start commands launched. Check the new windows for logs."