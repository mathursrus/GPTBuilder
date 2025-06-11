@echo off
echo ========================================
echo GPT Creator - Quick Run
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv_working\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup_working_environment.bat first
    pause
    exit /b 1
)

REM Check if config file is provided
if "%1"=="" (
    echo Usage: run_gpt_creator.bat [config-file.json]
    echo.
    echo Examples:
    echo   run_gpt_creator.bat test-gpt-config.json
    echo   run_gpt_creator.bat my-custom-gpt.json
    echo.
    pause
    exit /b 1
)

REM Check if config file exists
if not exist "%1" (
    echo ERROR: Config file '%1' not found!
    echo.
    echo Available config files:
    dir *.json /b 2>nul
    echo.
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv_working\Scripts\activate.bat

echo.
echo Running GPT Creator with config: %1
echo.
python gpt_creator_standalone.py %1

echo.
echo Script completed. Check the output above for results.
pause 