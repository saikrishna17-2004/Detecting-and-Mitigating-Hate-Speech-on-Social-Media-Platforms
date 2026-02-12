param(
    [int]$Port = 3000
)

Write-Host "Building frontend..." -ForegroundColor Cyan
npm run frontend:build
if ($LASTEXITCODE -ne 0) {
    Write-Host "Frontend build failed." -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host "Starting backend (production)..." -ForegroundColor Cyan
npm run backend:start:prod

Write-Host "Serving frontend build on http://localhost:$Port" -ForegroundColor Green
npx --yes serve frontend-react/build -l $Port
