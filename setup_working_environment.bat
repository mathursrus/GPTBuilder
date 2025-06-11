@echo off
echo ========================================
echo GPT Creator - Automated Setup
echo ========================================
echo.
echo This will install the EXACT working configuration:
echo - Python virtual environment
echo - Playwright 1.41.2 (the magic version!)
echo - Chromium browser
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul

echo.
echo [1/4] Creating virtual environment...
python -m venv venv_working
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    echo Make sure Python is installed and in your PATH
    pause
    exit /b 1
)
echo ✅ Virtual environment created

echo.
echo [2/4] Activating virtual environment...
call venv_working\Scripts\activate.bat
echo ✅ Virtual environment activated

echo.
echo [3/4] Installing Playwright 1.41.2 (this is the key!)...
pip install playwright==1.41.2
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Playwright
    pause
    exit /b 1
)
echo ✅ Playwright 1.41.2 installed

echo.
echo [4/4] Installing Chromium browser...
playwright install chromium
if %errorlevel% neq 0 (
    echo ERROR: Failed to install Chromium
    pause
    exit /b 1
)
echo ✅ Chromium browser installed

echo.
echo ========================================
echo 🎉 SETUP COMPLETE! 🎉
echo ========================================
echo.
echo Your GPT Creator is ready to use!
echo.
echo To test it:
echo 1. Open PowerShell/Command Prompt in this folder
echo 2. Run: venv_working\Scripts\activate
echo 3. Run: python gpt_creator_standalone.py test-gpt-config.json
echo.
echo The first run will ask you to login to ChatGPT.
echo Complete any CAPTCHA manually - this is normal!
echo.
echo Happy GPT creating! 🤖✨
echo.
pause 