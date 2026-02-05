# Setup development environment (Windows PowerShell)
# Usage: Open PowerShell in project root and run: .\scripts\setup_dev.ps1

param(
    [switch]$InstallNodeDeps
)

Write-Host "Creating virtual environment and installing Python packages..."
if (-Not (Test-Path -Path .venv)) {
    python -m venv .venv
}

. .\.venv\Scripts\Activate.ps1
pip install --upgrade pip
if (Test-Path requirements.txt) {
    pip install -r requirements.txt
} else {
    Write-Host "requirements.txt not found. Please create or install dependencies manually."
}

if ($InstallNodeDeps) {
    if (Test-Path frontend-react\package.json) {
        Write-Host "Installing frontend npm packages..."
        Push-Location frontend-react
        npm install
        Pop-Location
    } else {
        Write-Host "frontend-react/package.json not found. Skipping npm install."
    }
}

Write-Host "Setup complete. Activate with: . .\.venv\Scripts\Activate.ps1"