@echo off
echo ========================================
echo GPT Builder Script Setup
echo ========================================
echo.

echo Installing Python dependencies...
pip install playwright
if %errorlevel% neq 0 (
    echo ERROR: Failed to install playwright
    pause
    exit /b 1
)

echo.
echo Installing browser binaries...
echo (Setting browser path to match script requirements)
set PLAYWRIGHT_BROWSERS_PATH=%USERPROFILE%\.playwright-browsers
python -m playwright install chromium --with-deps
if %errorlevel% neq 0 (
    echo ERROR: Failed to install browsers
    pause
    exit /b 1
)

echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To test the script, run:
echo python gpt_creator_standalone.py test-gpt-config.json
echo.
pause 