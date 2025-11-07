@echo off
echo ============================================================
echo SmartHire - Quick Start
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.8+ and add it to your PATH.
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version
echo.

echo Starting SmartHire Application...
echo.
echo Application will be available at:
echo   http://localhost:5000
echo   http://127.0.0.1:5000
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

REM Run the application and capture any errors
python app.py
if errorlevel 1 (
    echo.
    echo [ERROR] An error occurred while running the application!
    echo Please check the error messages above.
    echo.
    pause
    exit /b 1
)

pause


