param(
  [int]$Port = 3002
)

<#
  Start React Frontend (port configurable; default 3002)
  ASCII-only output to avoid codepage issues.
#>
Write-Host "`nStarting React Frontend..." -ForegroundColor Cyan
Write-Host ("App will be available at: http://localhost:{0}`n" -f $Port) -ForegroundColor Green

# Move into React app folder
Set-Location -Path "frontend-react"

# Install dependencies if node_modules missing
if (-not (Test-Path -Path "node_modules")) {
  Write-Host "Installing dependencies (first run)..." -ForegroundColor Yellow
  npm install
}

# Set PORT for Windows PowerShell and start
$env:PORT = $Port
Write-Host ("Launching dev server on port {0}..." -f $Port) -ForegroundColor Green
# Use npm.cmd explicitly for Windows shells
& npm.cmd run start
