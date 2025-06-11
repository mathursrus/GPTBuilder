# 🚀 GPT Creator - Complete Setup Guide

This guide will get you up and running with the GPT Creator script in under 10 minutes!

## 📋 Prerequisites

- **Windows 10/11** (script tested on Windows)
- **Python 3.8 or higher** (any version works, including 3.12)
- **ChatGPT Plus subscription** (required for custom GPTs)
- **Internet connection**

## 🛠️ Quick Setup (5 Steps)

### Step 1: Download the Files
1. Download all files from this repository to a folder (e.g., `C:\GPTBuilder`)
2. Make sure you have these key files:
   - `gpt_creator_standalone.py`
   - `test-gpt-config.json`
   - `setup_working_environment.bat` (we'll create this)

### Step 2: Run the Setup Script
We'll create an automated setup script that installs the exact working configuration:

**Option A: Automatic Setup (Recommended)**
1. Double-click `setup_working_environment.bat`
2. Wait for it to complete (2-3 minutes)
3. Skip to Step 5

**Option B: Manual Setup**
If you prefer to do it manually, follow these commands in PowerShell/Command Prompt:

```bash
# Navigate to your GPTBuilder folder
cd C:\path\to\your\GPTBuilder

# Create virtual environment
python -m venv venv_working

# Activate it (Windows)
venv_working\Scripts\activate

# Install the EXACT working version (this is critical!)
pip install playwright==1.41.2

# Install the browser
playwright install chromium
```

### Step 3: Test the Setup
```bash
# Make sure you're in the virtual environment
venv_working\Scripts\activate

# Test with the sample configuration
python gpt_creator_standalone.py test-gpt-config.json
```

### Step 4: Login to ChatGPT
1. The script will open a browser window
2. **If you see a login page**: Log in manually to ChatGPT
3. **If you see a CAPTCHA**: Complete it manually (this is normal for first run)
4. The script will continue automatically after login

### Step 5: Success!
If everything works, you should see:
```
✅ GPT created successfully!
```

## 🎯 Creating Your Own GPT

### 1. Create Your Configuration File
Copy `test-gpt-config.json` and modify it:

```json
{
  "name": "My Awesome GPT",
  "description": "A helpful assistant that does amazing things",
  "instructions": "You are a helpful assistant that specializes in...",
  "conversation_starters": [
    "Hello! What can you help me with?",
    "How do you work?",
    "What are your capabilities?",
    "Can you give me an example?"
  ],
  "openapi_spec_file": "my_api_spec.json"
}
```

### 2. Run Your GPT Creation
```bash
# Activate environment
venv_working\Scripts\activate

# Create your GPT
python gpt_creator_standalone.py my-gpt-config.json
```

## 🔧 Troubleshooting

### "CAPTCHA keeps appearing"
- **Solution**: Make sure you're using Playwright 1.41.2 (not newer versions)
- **Check**: Run `pip list | findstr playwright` - should show `playwright 1.41.2`

### "Browser crashes" or "Page won't load"
- **Solution**: Delete `chatgpt_cookies.json` and try again
- **Alternative**: Restart your computer and try again

### "Can't find input fields"
- **Cause**: You might not be logged in properly
- **Solution**: Make sure you see your profile picture in the top-right of ChatGPT

### "Script says success but GPT wasn't created"
- **Check**: Go to https://chatgpt.com/gpts/mine to see your GPTs
- **Note**: Sometimes there's a delay before GPTs appear

## 📁 File Structure
After setup, your folder should look like this:
```
GPTBuilder/
├── venv_working/              # Virtual environment (auto-created)
├── gpt_creator_standalone.py  # Main script
├── test-gpt-config.json      # Sample configuration
├── chatgpt_cookies.json      # Login cookies (auto-created)
├── my-gpt-config.json        # Your custom config
└── SETUP_GUIDE.md           # This guide
```

## 🎉 Advanced Usage

### Adding Custom APIs
1. Create an OpenAPI 3.1.0 specification file
2. Reference it in your config: `"openapi_spec_file": "my_api.json"`
3. The script will automatically configure the GPT actions

### Updating Existing GPTs
- The script automatically detects existing GPTs with the same name
- It will update them instead of creating duplicates

### Running Multiple GPTs
```bash
# Create multiple GPTs in sequence
python gpt_creator_standalone.py gpt1-config.json
python gpt_creator_standalone.py gpt2-config.json
python gpt_creator_standalone.py gpt3-config.json
```

## ⚠️ Important Notes

1. **Always use the virtual environment** - Don't install globally
2. **Playwright 1.41.2 is critical** - Newer versions trigger bot detection
3. **ChatGPT Plus required** - Free accounts can't create custom GPTs
4. **One GPT at a time** - Don't run multiple instances simultaneously
5. **Keep browser visible** - Don't minimize during operation

## 🆘 Getting Help

If you run into issues:

1. **Check the logs** - The script shows detailed information about what it's doing
2. **Try the test config first** - Make sure the basic setup works
3. **Delete cookies** - Remove `chatgpt_cookies.json` and try again
4. **Restart fresh** - Close all browsers and try again

## 🔄 Updating

To update the script:
1. Download the new version
2. **Don't update Playwright** - Keep using 1.41.2
3. Test with your existing configuration

---

**That's it!** You should now have a fully working GPT Creator setup. The key is using Playwright 1.41.2 - this specific version bypasses ChatGPT's bot detection while newer versions get blocked.

Happy GPT creating! 🤖✨ 