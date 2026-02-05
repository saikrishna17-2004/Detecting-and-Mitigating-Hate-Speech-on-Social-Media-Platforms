# Activate virtual environment and run full backend
& "$PSScriptRoot\.venv\Scripts\Activate.ps1"
$env:RUN_BACKEND_DIRECT = '1'
python "$PSScriptRoot\run_backend.py"
