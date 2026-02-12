# Deployment Pre-flight Checklist Script
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Deployment Pre-flight Check" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$passed = 0
$failed = 0

# Check 1: Git repository
Write-Host "[1/7] Checking Git repository..." -ForegroundColor Yellow
if (Test-Path ".git") {
    Write-Host "  ✓ Git repository found" -ForegroundColor Green
    $passed++
} else {
    Write-Host "  ✗ Not a Git repository" -ForegroundColor Red
    $failed++
}

# Check 2: Requirements.txt
Write-Host "[2/7] Checking requirements.txt..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    Write-Host "  ✓ requirements.txt found" -ForegroundColor Green
    $passed++
} else {
    Write-Host "  ✗ requirements.txt missing" -ForegroundColor Red
    $failed++
}

# Check 3: Procfile
Write-Host "[3/7] Checking Procfile..." -ForegroundColor Yellow
if (Test-Path "Procfile") {
    $procContent = Get-Content "Procfile" -Raw
    if ($procContent -match "gunicorn") {
        Write-Host "  ✓ Procfile configured correctly" -ForegroundColor Green
        $passed++
    } else {
        Write-Host "  ✗ Procfile missing gunicorn command" -ForegroundColor Red
        $failed++
    }
} else {
    Write-Host "  ✗ Procfile not found" -ForegroundColor Red
    $failed++
}

# Check 4: Frontend build directory
Write-Host "[4/7] Checking frontend structure..." -ForegroundColor Yellow
if (Test-Path "frontend-react\package.json") {
    Write-Host "  ✓ Frontend package.json found" -ForegroundColor Green
    $passed++
} else {
    Write-Host "  ✗ Frontend package.json missing" -ForegroundColor Red
    $failed++
}

# Check 5: Backend app
Write-Host "[5/7] Checking backend app..." -ForegroundColor Yellow
if (Test-Path "backend\app.py") {
    Write-Host "  ✓ Backend app.py found" -ForegroundColor Green
    $passed++
} else {
    Write-Host "  ✗ Backend app.py missing" -ForegroundColor Red
    $failed++
}

# Check 6: ML Model files
Write-Host "[6/7] Checking ML model files..." -ForegroundColor Yellow
if ((Test-Path "ml_model\hate_speech_model.pkl") -or (Test-Path "ml_model\*.pkl")) {
    Write-Host "  ✓ ML model found" -ForegroundColor Green
    $passed++
} else {
    Write-Host "  ⚠ ML model not found (will be loaded on first run)" -ForegroundColor Yellow
    $passed++
}

# Check 7: Git status
Write-Host "[7/7] Checking Git status..." -ForegroundColor Yellow
$gitStatus = git status --porcelain
if ($LASTEXITCODE -eq 0) {
    if ($gitStatus) {
        Write-Host "  ⚠ Uncommitted changes detected" -ForegroundColor Yellow
        Write-Host "    Run: git add . && git commit -m 'Ready for deployment'" -ForegroundColor Gray
    } else {
        Write-Host "  ✓ All changes committed" -ForegroundColor Green
    }
    $passed++
} else {
    Write-Host "  ⚠ Cannot check Git status" -ForegroundColor Yellow
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Passed: $passed" -ForegroundColor Green
if ($failed -gt 0) {
    Write-Host "Failed: $failed" -ForegroundColor Red
}

if ($failed -eq 0) {
    Write-Host "`n✓ Project is ready for deployment!`n" -ForegroundColor Green
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Push to GitHub: git push origin main" -ForegroundColor White
    Write-Host "  2. Follow deployment guide: DEPLOYMENT_WALKTHROUGH.md" -ForegroundColor White
    Write-Host "`n  Quick start:" -ForegroundColor Yellow
    Write-Host "    - Backend: https://render.com (Web Service)" -ForegroundColor Gray
    Write-Host "    - Frontend: https://netlify.com (New Site)" -ForegroundColor Gray
} else {
    Write-Host "`n✗ Please fix the issues above before deploying`n" -ForegroundColor Red
}

Write-Host "`n"
