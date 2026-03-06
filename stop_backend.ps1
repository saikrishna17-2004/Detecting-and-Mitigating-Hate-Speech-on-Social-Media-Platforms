# Stop Backend Server
# This script stops the backend server if it's running

Write-Host "`nStopping Backend Server..." -ForegroundColor Cyan

# Stop process listening on backend port first (most reliable)
$listenerPids = Get-NetTCPConnection -LocalPort 5000 -State Listen -ErrorAction SilentlyContinue |
    Select-Object -ExpandProperty OwningProcess -Unique

foreach ($pid in $listenerPids) {
    try {
        Stop-Process -Id $pid -Force -ErrorAction Stop
        Write-Host "Stopped listener process PID: $pid" -ForegroundColor Green
    } catch {
    }
}

# Fallback: stop known backend python processes by commandline
$backendProcess = Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
    Where-Object {
        $_.Name -match '^python(\.exe)?$' -and (
            $_.CommandLine -like '*run_backend.py*' -or
            $_.CommandLine -like '*run_flask_dev.py*' -or
            $_.CommandLine -like '*server.py*' -or
            $_.CommandLine -like '*backend\\app.py*'
        )
    }

if ($backendProcess) {
    foreach ($proc in $backendProcess) {
        try {
            Stop-Process -Id $proc.ProcessId -Force -ErrorAction Stop
            Write-Host "Stopped backend process PID: $($proc.ProcessId)" -ForegroundColor Green
        } catch {
        }
    }
} else {
    if (-not $listenerPids) {
        Write-Host "Backend server is not running" -ForegroundColor Yellow
    }
}
