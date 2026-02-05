# Quick Start Script
# This script sets up and runs the entire application

Write-Host "`n==================================" -ForegroundColor Cyan
Write-Host "Hate Speech Detection System" -ForegroundColor Cyan
Write-Host "Quick Start Script" -ForegroundColor Cyan
Write-Host "==================================`n" -ForegroundColor Cyan

# Check if virtual environment exists
if (-Not (Test-Path ".venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Install dependencies
Write-Host "`nInstalling dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Train the model
Write-Host "`nTraining ML model..." -ForegroundColor Yellow
python ml_model\train_model.py

Write-Host "`n==================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "==================================`n" -ForegroundColor Green

Write-Host "To start the application:" -ForegroundColor Cyan
Write-Host "1. Backend API: python backend\app.py" -ForegroundColor White
Write-Host "2. Frontend Dashboard: streamlit run frontend\app.py" -ForegroundColor White
Write-Host ""
