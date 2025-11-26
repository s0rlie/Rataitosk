@echo off
setlocal enabledelayedexpansion

echo ==========================================
echo    🐿️  Installing Rataitosk (Windows)
echo ==========================================

REM 1. Check Python presence
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python not found on this system.
    echo 💡 You can:
    echo    1. Ask IT to install Python 3.9+ from https://www.python.org/downloads/
    echo    2. Use the fallback 'python-portable\' folder if included.
    echo.
    echo Aborting setup.
    pause
    exit /b 1
)

REM 2. Check Python version (>= 3.9)
for /f "tokens=2 delims= " %%v in ('python --version 2^>nul') do set VER=%%v
for /f "tokens=1,2 delims=." %%a in ("!VER!") do (
    set MAJOR=%%a
    set MINOR=%%b
)

if !MAJOR! LSS 3 (
    echo ❌ Python version too old: !VER!
    exit /b 1
)

if !MAJOR! EQU 3 if !MINOR! LSS 9 (
    echo ❌ Python version must be 3.9 or newer. Found: !VER!
    exit /b 1
)

echo ✅ Python version !VER! is OK.

REM 3. Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to create virtual environment.
    echo Developer note: Make sure Python's 'venv' module is installed.
    pause
    exit /b 1
)

REM 4. Activate and install dependencies
call venv\Scripts\activate.bat

echo Installing packages (this may take a few minutes)...
pip install --upgrade pip
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Failed to upgrade pip
    pause
    exit /b 1
)

pip install -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Package installation failed.
    pause
    exit /b 1
)

echo.
echo ✅ Rataitosk is installed and ready.

echo.
echo ➤ To run the tool:
echo    1. Place two PDFs into the input\ folder
echo    2. Run: cli\run_rataitosk.py (double-click or use command line)
echo.

pause