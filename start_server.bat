@echo off
REM ==================================================================
REM Start backend server in a NEW PowerShell window and return immediately
REM ==================================================================

setlocal ENABLEDELAYEDEXPANSION

REM Determine project root (this batch's directory)
set "PROJ_DIR=%~dp0"
pushd "%PROJ_DIR%"

echo ============================================================
echo Launching Hate Speech Detection Backend Server (new window)
echo ============================================================

REM Use PowerShell to activate venv and run full backend with waitress
REM -NoExit keeps the window open so the server persists
start "Hate Speech API" powershell -NoExit -Command ^
	"cd '%PROJ_DIR:'=%'; ^
	 .\.venv\Scripts\Activate.ps1; ^
	 $env:RUN_BACKEND_DIRECT='1'; python run_backend.py"

echo Started. A new PowerShell window should now be running the server.
echo If you don't see it, check your taskbar or alt-tab.
echo Server URL: http://localhost:5000
echo.
echo Tip: Run 'python test_backend_api.py' here to verify the API.

popd
endlocal

exit /b 0
