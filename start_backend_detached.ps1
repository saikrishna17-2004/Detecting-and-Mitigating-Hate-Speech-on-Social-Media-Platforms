<#
  Deprecated detached helper. Use start_server.bat instead.
  This script now delegates to start_server.bat.
#>
Write-Host "`nStarting Backend API Server (Detached Mode)..." -ForegroundColor Cyan
$pythonExe = "C:/Users/nakka/Desktop/pp1/.venv/Scripts/python.exe"
$startedByBatch = $false

if (Test-Path -Path "start_server.bat") {
  Start-Process -FilePath "start_server.bat"
  $startedByBatch = $true
  Write-Host "A new PowerShell window should now be running the server." -ForegroundColor Green
} else {
  Write-Host "start_server.bat not found. Trying direct Python launch..." -ForegroundColor Yellow
}

$maxWaitSeconds = 20
$isListening = $false

for ($i = 1; $i -le $maxWaitSeconds; $i++) {
  $listener = Get-NetTCPConnection -LocalPort 5000 -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($listener) {
    $isListening = $true
    break
  }
  Start-Sleep -Seconds 1
}

if ($isListening) {
  Write-Host "Backend startup verified: listening on http://localhost:5000" -ForegroundColor Green
} else {
  Write-Host "Batch launch did not start backend within $maxWaitSeconds seconds." -ForegroundColor Yellow
  Write-Host "Trying direct detached Python start..." -ForegroundColor Yellow

  if (-not (Test-Path -Path $pythonExe)) {
    Write-Host "Python executable not found at $pythonExe" -ForegroundColor Red
    exit 1
  }

  Start-Process -FilePath $pythonExe -ArgumentList "run_backend.py" -WorkingDirectory (Get-Location).Path -WindowStyle Hidden

  $isListening = $false
  for ($i = 1; $i -le $maxWaitSeconds; $i++) {
    $listener = Get-NetTCPConnection -LocalPort 5000 -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($listener) {
      $isListening = $true
      break
    }
    Start-Sleep -Seconds 1
  }

  if ($isListening) {
    Write-Host "Backend startup verified via direct Python launch: http://localhost:5000" -ForegroundColor Green
  } else {
    if ($startedByBatch) {
      Write-Host "Check the spawned backend window for startup errors." -ForegroundColor Yellow
    }
    Write-Host "Backend failed to start listening on port 5000." -ForegroundColor Red
    exit 1
  }
}
