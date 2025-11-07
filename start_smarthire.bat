@echo off
echo ============================================================
echo SmartHire - Complete Setup and Launch Script
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

REM Check if MySQL is accessible (optional check)
echo [INFO] Checking MySQL connection...
python -c "import pymysql; pymysql.connect(host='localhost', user='root', password='')" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Could not connect to MySQL. Please ensure XAMPP MySQL is running.
    echo [WARNING] Continuing anyway - database setup will be attempted...
) else (
    echo [OK] MySQL connection successful
)
echo.

REM Step 1: Install Python dependencies
echo ============================================================
echo Step 1: Installing Python Dependencies
echo ============================================================
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies!
    echo [INFO] Trying without --quiet flag for better error messages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies!
        pause
        exit /b 1
    )
)
echo [OK] Dependencies installed successfully
echo.

REM Step 2: Download spaCy language model
echo ============================================================
echo Step 2: Installing spaCy Language Model
echo ============================================================
echo.
python -c "import spacy; spacy.load('en_core_web_sm')" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Downloading spaCy model (this may take a few minutes)...
    pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl
    if errorlevel 1 (
        echo [WARNING] Failed to install spaCy model. Some features may not work.
        echo [INFO] You can manually install it later with:
        echo        pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1-py3-none-any.whl
    ) else (
        echo [OK] spaCy model installed
    )
) else (
    echo [OK] spaCy model already installed
)
echo.

REM Step 3: Setup Database
echo ============================================================
echo Step 3: Setting Up Database
echo ============================================================
echo.
python setup_database.py
if errorlevel 1 (
    echo [ERROR] Database setup failed!
    pause
    exit /b 1
)
echo.

REM Step 4: Initialize Database Tables
echo ============================================================
echo Step 4: Initializing Database Tables
echo ============================================================
echo.
python init_db.py
if errorlevel 1 (
    echo [ERROR] Failed to initialize database tables!
    pause
    exit /b 1
)
echo.

REM Step 5: Create Test Users (if they don't exist)
echo ============================================================
echo Step 5: Creating Test Users
echo ============================================================
echo.
python create_test_users.py
echo.

REM Step 6: Fix any plain text passwords
echo ============================================================
echo Step 6: Ensuring Password Security
echo ============================================================
echo.
python fix_passwords.py
echo.

REM Step 7: Start the Flask Application
echo ============================================================
echo Step 7: Starting SmartHire Application
echo ============================================================
echo.
echo [SUCCESS] All setup completed!
echo.
echo ============================================================
echo SmartHire is starting...
echo ============================================================
echo.
echo Application will be available at:
echo   http://localhost:5000
echo   http://127.0.0.1:5000
echo.
echo Test Login Credentials:
echo   Admin:     username=admin, password=admin123
echo   Applicant: username=applicant1, password=applicant123
echo   Employer:  username=employer1, password=employer123
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

REM Start Flask application
python app.py

pause

