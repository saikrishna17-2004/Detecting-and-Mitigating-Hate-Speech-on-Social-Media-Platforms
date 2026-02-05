@echo off
echo.
echo ========================================
echo  Starting Backend Server (Persistent)
echo ========================================
echo.

cd /d "%~dp0"

REM Activate virtual environment and run server
call .venv\Scripts\activate.bat

echo Starting Flask server...
echo Server will run on http://localhost:5000
echo.
echo To stop the server, close this window
echo.

python backend\app.py

pause
