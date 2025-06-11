# 🤖 GPT Creator - Automated Custom GPT Builder

**Automatically create and update custom GPTs on ChatGPT using browser automation.**

This tool lets you programmatically create custom GPTs with:
- ✅ Custom names, descriptions, and instructions
- ✅ Conversation starters
- ✅ API integrations (OpenAPI specs)
- ✅ Automatic updates to existing GPTs
- ✅ Bypasses bot detection (using the right Playwright version!)

## 🚀 Quick Start

1. **Download** all files to a folder
2. **Run** `setup_working_environment.bat` 
3. **Test** with `run_gpt_creator.bat test-gpt-config.json`

That's it! 🎉

## 📖 Full Documentation

👉 **[Complete Setup Guide](SETUP_GUIDE.md)** - Everything you need to know

## 🎯 What You Need

- Windows 10/11
- Python 3.8+
- ChatGPT Plus subscription
- 5 minutes for setup

## 🔧 Key Files

- `gpt_creator_standalone.py` - Main script
- `setup_working_environment.bat` - One-click setup
- `run_gpt_creator.bat` - Easy way to run the script
- `test-gpt-config.json` - Sample configuration
- `SETUP_GUIDE.md` - Detailed instructions

## ⚡ Quick Example

```bash
# Setup (run once)
setup_working_environment.bat

# Create a GPT
run_gpt_creator.bat my-gpt-config.json
```

## 🎨 Sample Configuration

```json
{
  "name": "My Helper Bot",
  "description": "A helpful assistant for daily tasks",
  "instructions": "You are a friendly assistant that helps with...",
  "conversation_starters": [
    "Hello! How can I help you today?",
    "What can you do for me?"
  ]
}
```

## 🔑 The Secret Sauce

This tool works because it uses **Playwright 1.41.2** - the exact version that bypasses ChatGPT's bot detection. Newer versions get blocked by CAPTCHAs, but this version works perfectly!

## 🆘 Need Help?

Check the [Setup Guide](SETUP_GUIDE.md) for troubleshooting and detailed instructions.

---

**Happy GPT creating!** 🤖✨ 