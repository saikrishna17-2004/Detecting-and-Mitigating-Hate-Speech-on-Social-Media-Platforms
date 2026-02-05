# Start Frontend Dashboard
Write-Host "`n🎨 Starting Frontend Dashboard..." -ForegroundColor Cyan
Write-Host "Dashboard will be available at: http://localhost:8501`n" -ForegroundColor Green

# Activate virtual environment
& .\.venv\Scripts\Activate.ps1

# Run frontend
streamlit run frontend\app.py
