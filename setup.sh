#!/bin/bash

echo "========================================"
echo "GPT Builder Script Setup"
echo "========================================"
echo

echo "Installing Python dependencies..."
pip install playwright
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install playwright"
    echo "Try using pip3 instead of pip, or install with --user flag"
    exit 1
fi

echo
echo "Installing browser binaries..."
echo "(Setting browser path to match script requirements)"
export PLAYWRIGHT_BROWSERS_PATH="$HOME/.playwright-browsers"
python -m playwright install chromium --with-deps
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install browsers"
    exit 1
fi

echo
echo "========================================"
echo "Setup completed successfully!"
echo "========================================"
echo
echo "To test the script, run:"
echo "python gpt_creator_standalone.py test-gpt-config.json"
echo

# Make the script executable
chmod +x "$0" 