# Pre-Deployment Verification Script

Write-Host ""
Write-Host "========================================"
Write-Host "   DEPLOYMENT READINESS CHECK" -ForegroundColor Cyan
Write-Host "========================================"
Write-Host ""

$allGood = $true

# Check Git
Write-Host "Checking Git repository..." -ForegroundColor Yellow
if (Test-Path ".git") {
    Write-Host "[OK] Git repository found" -ForegroundColor Green
    $remote = git remote get-url origin 2>$null
    if ($remote) {
        Write-Host "[OK] Git remote: $remote" -ForegroundColor Green
    }
} else {
    Write-Host "[FAIL] Not a git repository" -ForegroundColor Red
    $allGood = $false
}

# Check required files
Write-Host ""
Write-Host "Checking required files..." -ForegroundColor Yellow
$requiredFiles = @("requirements.txt", "Procfile", "run_backend.py", "frontend-react/package.json", ".env")
foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "[OK] $file" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] $file missing" -ForegroundColor Red
        $allGood = $false
    }
}

# Check Python dependencies
Write-Host ""
Write-Host "Checking Python dependencies..." -ForegroundColor Yellow
$gunicorn = python -c "import gunicorn; print(gunicorn.__version__)" 2>$null
if ($gunicorn) {
    Write-Host "[OK] gunicorn installed (v$gunicorn)" -ForegroundColor Green
} else {
    Write-Host "[FAIL] gunicorn not installed" -ForegroundColor Red
    $allGood = $false
}

$pymongo = python -c "import pymongo; print(pymongo.__version__)" 2>$null
if ($pymongo) {
    Write-Host "[OK] pymongo installed (v$pymongo)" -ForegroundColor Green
} else {
    Write-Host "[FAIL] pymongo not installed" -ForegroundColor Red
    $allGood = $false
}

# Check environment variables
Write-Host ""
Write-Host "Checking .env configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    if ($envContent -match "DATABASE_URL=mongodb") {
        Write-Host "[OK] MongoDB connection string configured" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] DATABASE_URL not configured" -ForegroundColor Red
        $allGood = $false
    }
}

# Summary
Write-Host ""
Write-Host "========================================"
if ($allGood) {
    Write-Host "   READY TO DEPLOY!" -ForegroundColor Green
} else {
    Write-Host "   FIX ISSUES BEFORE DEPLOYING" -ForegroundColor Red
}
Write-Host "========================================"
Write-Host ""

# Show environment variables for Render
Write-Host "Production Environment Variables" -ForegroundColor Cyan
Write-Host "Copy these to your Render dashboard:"
Write-Host ""
Write-Host "SECRET_KEY=ib90onHydhLh8cpoAUYLIyA0bAVQrKb7BVSYcRMISsg"
Write-Host "JWT_SECRET_KEY=JJFEZ6Cvc1YhQ45nRsm2mMaqyPURX-sFrGMHfBohr9A"
Write-Host "DATABASE_URL=mongodb+srv://SAIKRISHNA:YadavNakkala@cluster0.osgwmcy.mongodb.net/hate_speech_db?retryWrites=true&w=majority"
Write-Host "FLASK_ENV=production"
Write-Host "FRONTEND_URL=https://your-netlify-site.netlify.app"
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Read DEPLOYMENT_CHECKLIST.md for full instructions"
Write-Host "2. Push code: git push origin main"
Write-Host "3. Deploy on Render.com (backend)"
Write-Host "4. Deploy on Netlify.com (frontend)"
Write-Host ""
