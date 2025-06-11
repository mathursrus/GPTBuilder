# Quick Start Guide

Get your GPT Builder script running in 5 minutes!

## 🚀 Quick Setup

### 1. Install Dependencies (One-Time Setup)

**Windows:**
```bash
setup.bat
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

> 💡 **You only need to run this once!** After setup, just run the Python script directly.

**Manual Installation:**
```bash
pip install playwright
# Set the browser path to match the script
set PLAYWRIGHT_BROWSERS_PATH=%USERPROFILE%\.playwright-browsers  # Windows
export PLAYWRIGHT_BROWSERS_PATH="$HOME/.playwright-browsers"     # macOS/Linux
python -m playwright install chromium --with-deps
```

### 2. Test Run
```bash
python gpt_creator_standalone.py test-gpt-config.json
```

### 3. Login When Prompted
- Browser will open automatically
- Log into ChatGPT manually
- Script continues automatically after login

## ✅ What Happens Next

1. **Browser opens** → Log into ChatGPT
2. **Script runs** → Creates "Try this GPT" 
3. **Success!** → Your test GPT is ready

## 🎯 Create Your Own GPT

### 1. Copy the test config:
```bash
cp test-gpt-config.json my-gpt-config.json
```

### 2. Edit your config:
```json
{
  "name": "My Awesome GPT",
  "description": "What my GPT does",
  "instructions": "You are a helpful assistant that...",
  "conversation_starters": [
    "Hello! What can you do?",
    "How can you help me?"
  ]
}
```

### 3. Run with your config:
```bash
python gpt_creator_standalone.py my-gpt-config.json
```

## 🔧 Troubleshooting

**Script fails?** → Delete `chatgpt_cookies.json` and try again

**Need help?** → Check the full README.md

## 📋 Requirements

- Python 3.7+
- ChatGPT Plus subscription
- Internet connection

That's it! 🎉 