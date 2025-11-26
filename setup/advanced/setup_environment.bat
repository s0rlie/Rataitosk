REM Developer-only script. Not intended for general users.

@echo off
setlocal

echo ==========================================
echo   🐿️  Quick Environment Setup (Dev Use Only)
echo ==========================================

REM Assumes Python 3.9+ is already installed and available

python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to create virtual environment.
    exit /b 1
)

call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

echo ✅ Environment is ready.
echo To run: python cli\run_rataitosk.py