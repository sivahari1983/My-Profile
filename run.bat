@echo off
setlocal enabledelayedexpansion

echo.
echo ============================================================================
echo Portfolio Website - Running Application
echo ============================================================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found. Running setup...
    call setup.bat
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies if needed
pip install -r requirements.txt --quiet

echo.
echo Starting Flask application...
echo.
echo ============================================================================
echo Server is running!
echo ============================================================================
echo.
echo Open your browser and navigate to:
echo   http://localhost:5000
echo.
echo To upload your PDF profile:
echo 1. Scroll to bottom of the page
echo 2. Click "Upload Your Profile PDF"
echo 3. Select your PDF file
echo 4. Click "Process PDF"
echo.
echo Press CTRL+C to stop the server
echo.

python app.py
