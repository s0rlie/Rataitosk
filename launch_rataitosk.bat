@echo off
setlocal

echo ==========================================
echo   🐿️  Launching Rataitosk
echo ==========================================

REM 1. Check venv exists
if not exist "venv\" (
    echo ❌ Virtual environment not found.
    echo 💡 Please run setup\install_rataitosk.bat first.
    pause
    exit /b 1
)

REM 2. Activate venv
call venv\Scripts\activate.bat

REM 3. Run the CLI
echo Running document comparison tool...
python cli\run_rataitosk.py

echo.
echo ✅ Finished. Results saved in \output
pause