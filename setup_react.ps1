# React Frontend Setup Script
Write-Host "`n🚀 Setting up React Frontend..." -ForegroundColor Cyan

# Navigate to frontend-react directory
Set-Location frontend-react

# Install dependencies
Write-Host "`n📦 Installing dependencies..." -ForegroundColor Yellow
npm install

Write-Host "`n✅ React frontend setup complete!" -ForegroundColor Green
Write-Host "`nTo start the development server:" -ForegroundColor Cyan
Write-Host "  cd frontend-react" -ForegroundColor White
Write-Host "  npm start" -ForegroundColor White
Write-Host "`nThe app will run on http://localhost:3000" -ForegroundColor Green
