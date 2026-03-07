# Pre-Deployment Verification Script
# Run this before deploying to check everything is ready

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "🚀 DEPLOYMENT READINESS CHECK" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$allGood = $true

# Check 1: Git repository
Write-Host "Checking Git repository..." -ForegroundColor Yellow
if (Test-Path ".git") {
    Write-Host "✅ Git repository found" -ForegroundColor Green
    
    # Check for uncommitted changes
    $status = git status --porcelain
    if ($status) {
        Write-Host "⚠️  Warning: You have uncommitted changes" -ForegroundColor Yellow
        Write-Host "   Run: git add . && git commit -m 'Prepare for deployment' && git push" -ForegroundColor Gray
    } else {
        Write-Host "✅ No uncommitted changes" -ForegroundColor Green
    }
    
    # Check remote
    $remote = git remote get-url origin 2>$null
    if ($remote) {
        Write-Host "✅ Git remote: $remote" -ForegroundColor Green
    } else {
        Write-Host "❌ No git remote configured" -ForegroundColor Red
        $allGood = $false
    }
} else {
    Write-Host "❌ Not a git repository" -ForegroundColor Red
    $allGood = $false
}

# Check 2: Required files
Write-Host "`nChecking required files..." -ForegroundColor Yellow
$requiredFiles = @(
    "requirements.txt",
    "Procfile",
    "run_backend.py",
    "frontend-react/package.json",
    ".env"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "✅ $file" -ForegroundColor Green
    } else {
        Write-Host "❌ $file missing" -ForegroundColor Red
        $allGood = $false
    }
}

# Check 3: Python dependencies
Write-Host "`nChecking Python dependencies..." -ForegroundColor Yellow
try {
    $gunicorn = python -c "import gunicorn; print(gunicorn.__version__)" 2>$null
    if ($gunicorn) {
        Write-Host "✅ gunicorn installed (v$gunicorn)" -ForegroundColor Green
    } else {
        Write-Host "❌ gunicorn not installed" -ForegroundColor Red
        $allGood = $false
    }
} catch {
    Write-Host "❌ Error checking gunicorn" -ForegroundColor Red
    $allGood = $false
}

try {
    $pymongo = python -c "import pymongo; print(pymongo.__version__)" 2>$null
    if ($pymongo) {
        Write-Host "✅ pymongo installed (v$pymongo)" -ForegroundColor Green
    } else {
        Write-Host "❌ pymongo not installed" -ForegroundColor Red
        $allGood = $false
    }
} catch {
    Write-Host "❌ Error checking pymongo" -ForegroundColor Red
    $allGood = $false
}

# Check 4: Frontend dependencies
Write-Host "`nChecking Frontend..." -ForegroundColor Yellow
if (Test-Path "frontend-react/node_modules") {
    Write-Host "✅ Node modules installed" -ForegroundColor Green
} else {
    Write-Host "⚠️  Node modules not found. Run: cd frontend-react && npm install" -ForegroundColor Yellow
}

# Check 5: Environment variables
Write-Host "`nChecking .env configuration..." -ForegroundColor Yellow
if (Test-Path ".env") {
    $envContent = Get-Content ".env" -Raw
    
    if ($envContent -match "DATABASE_URL=mongodb") {
        Write-Host "✅ MongoDB connection string configured" -ForegroundColor Green
    } else {
        Write-Host "❌ DATABASE_URL not configured in .env" -ForegroundColor Red
        $allGood = $false
    }
    
    if ($envContent -match "SECRET_KEY=") {
        Write-Host "✅ SECRET_KEY configured" -ForegroundColor Green
    } else {
        Write-Host "⚠️  SECRET_KEY not configured" -ForegroundColor Yellow
    }
    
    if ($envContent -match "JWT_SECRET_KEY=") {
        Write-Host "✅ JWT_SECRET_KEY configured" -ForegroundColor Green
    } else {
        Write-Host "⚠️  JWT_SECRET_KEY not configured" -ForegroundColor Yellow
    }
}

# Check 6: ML Model
Write-Host "`nChecking ML Model..." -ForegroundColor Yellow
if (Test-Path "ml_model/hate_speech_model.pkl") {
    Write-Host "✅ ML model found" -ForegroundColor Green
} else {
    Write-Host "⚠️  ML model not found (will be trained on first run)" -ForegroundColor Yellow
}

# Summary
Write-Host "`n========================================" -ForegroundColor Cyan
if ($allGood) {
    Write-Host "✅ ALL CHECKS PASSED - READY TO DEPLOY!" -ForegroundColor Green
    Write-Host "`nNext steps:" -ForegroundColor Cyan
    Write-Host "1. Review DEPLOYMENT_CHECKLIST.md" -ForegroundColor White
    Write-Host "2. Push to GitHub: git push origin main" -ForegroundColor White
    Write-Host "3. Deploy backend on Render.com" -ForegroundColor White
    Write-Host "4. Deploy frontend on Netlify.com" -ForegroundColor White
} else {
    Write-Host "❌ SOME CHECKS FAILED - FIX ISSUES BEFORE DEPLOYING" -ForegroundColor Red
}
Write-Host "========================================`n" -ForegroundColor Cyan

# Display safe env var template for production
Write-Host "Production Environment Variables template:" -ForegroundColor Cyan
Write-Host "Copy these keys to your Render dashboard and set secure values:" -ForegroundColor Gray
Write-Host ""
Write-Host "SECRET_KEY=<generate-random-secret>" -ForegroundColor Yellow
Write-Host "JWT_SECRET_KEY=<generate-random-secret>" -ForegroundColor Yellow
Write-Host "DATABASE_URL=<your-mongodb-atlas-connection-string>" -ForegroundColor Yellow
Write-Host "FLASK_ENV=production" -ForegroundColor Yellow
Write-Host "FRONTEND_URL=https://your-netlify-site.netlify.app" -ForegroundColor Yellow
Write-Host ""
Write-Host "(Update FRONTEND_URL after frontend deployment)" -ForegroundColor Gray
Write-Host ""




