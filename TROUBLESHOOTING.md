# Troubleshooting Guide

Common issues and solutions for the GPT Builder script.

## 🚨 Installation Issues

### Python Not Found
**Error:** `'python' is not recognized as an internal or external command`

**Solutions:**
- Install Python from [python.org](https://python.org)
- Add Python to your system PATH
- Try using `python3` instead of `python`
- On Windows, try `py` instead of `python`

### Pip Not Found
**Error:** `'pip' is not recognized as an internal or external command`

**Solutions:**
- Try `python -m pip install playwright`
- Try `python3 -m pip install playwright`
- Reinstall Python with "Add to PATH" option checked

### Playwright Installation Fails
**Error:** `Failed to install playwright`

**Solutions:**
```bash
# Try with user flag
pip install --user playwright

# Try with specific Python version
python3 -m pip install playwright

# Force reinstall
pip install --force-reinstall playwright
```

### Browser Installation Fails
**Error:** `Failed to install chromium` or `Executable doesn't exist at ...\.playwright-browsers\`

**Solutions:**
```bash
# Set the correct browser path first
set PLAYWRIGHT_BROWSERS_PATH=%USERPROFILE%\.playwright-browsers     # Windows
export PLAYWRIGHT_BROWSERS_PATH="$HOME/.playwright-browsers"        # macOS/Linux

# Then install with Python module syntax
python -m playwright install chromium --with-deps --force

# Or use the setup scripts
setup.bat        # Windows
./setup.sh       # macOS/Linux
```

**Why this happens:** The script uses a custom browser installation path that must match where Playwright installs the browsers.

**Important:** You only need to run the setup script once. After that, the Python script automatically sets the correct browser path every time it runs.

## 🔐 Login & Authentication Issues

### Can't Login to ChatGPT
**Symptoms:** Browser opens but login fails or hangs

**Solutions:**
1. **Clear cookies:** Delete `chatgpt_cookies.json`
2. **Manual login:** Log in manually when browser opens
3. **Check subscription:** Ensure you have ChatGPT Plus
4. **Try incognito:** Close all ChatGPT tabs and try again
5. **VPN issues:** Disable VPN if using one

### Cloudflare CAPTCHA Challenge
**Symptoms:** "Verify you are human" page appears

**Solutions:**
1. **Complete the CAPTCHA:** Simply click the checkbox - this is normal
2. **Wait for verification:** The script will continue after you pass
3. **Don't close browser:** Let the script proceed after CAPTCHA completion

**Prevention:**
- **Wait between runs:** Don't run the script too frequently
- **Use saved cookies:** Let the script save your session
- **Clear browser data:** If CAPTCHAs persist, delete `chatgpt_cookies.json`
- **Different network:** Try from a different IP if issues continue

### Session Expired
**Error:** Script fails after working previously

**Solutions:**
1. Delete `chatgpt_cookies.json`
2. Run script again and login manually
3. Check if your ChatGPT Plus subscription is active

## 🤖 Browser & Automation Issues

### Browser Crashes
**Error:** `Browser has crashed or become unresponsive`

**Solutions:**
1. **Close other browsers:** Close Chrome/Edge instances
2. **Free memory:** Close unnecessary applications
3. **Restart computer:** If memory issues persist
4. **Update browser:** Ensure Chrome is up to date

### Browser Won't Start
**Error:** Browser fails to launch

**Solutions:**
```bash
# Reinstall browser
playwright install --force chromium

# Check system requirements
playwright install-deps

# Try different browser
# (Edit script to use 'firefox' instead of 'chromium')
```

### Script Hangs
**Symptoms:** Script stops responding

**Solutions:**
1. **Wait longer:** Some operations take time
2. **Check browser:** Look for popup dialogs
3. **Restart script:** Ctrl+C and run again
4. **Clear cookies:** Delete `chatgpt_cookies.json`

## 📝 Configuration Issues

### Invalid JSON
**Error:** `JSON decode error`

**Solutions:**
1. **Validate JSON:** Use [jsonlint.com](https://jsonlint.com)
2. **Check quotes:** Use double quotes, not single
3. **Check commas:** No trailing commas allowed
4. **Check encoding:** Save file as UTF-8

### Missing Required Fields
**Error:** Script fails to create GPT

**Solutions:**
Ensure your config has all required fields:
```json
{
  "name": "Required - GPT name",
  "description": "Required - GPT description", 
  "instructions": "Required - GPT instructions"
}
```

### OpenAPI Validation Fails
**Error:** API configuration rejected

**Solutions:**
1. **Validate spec:** Use [swagger.io/tools/swagger-editor](https://editor.swagger.io)
2. **Check version:** Must be OpenAPI 3.1.0
3. **Check URLs:** Ensure server URLs are accessible
4. **Test endpoints:** Verify your API works

## 🌐 Network Issues

### Connection Timeout
**Error:** Network timeouts or connection refused

**Solutions:**
1. **Check internet:** Verify connection works
2. **Firewall:** Allow Python/Playwright through firewall
3. **Proxy:** Configure proxy settings if needed
4. **DNS:** Try different DNS servers (8.8.8.8)

### Rate Limiting
**Error:** Too many requests

**Solutions:**
1. **Wait:** OpenAI may be rate limiting
2. **Retry later:** Try again in a few minutes
3. **Check status:** Visit [status.openai.com](https://status.openai.com)

## 🖥️ Platform-Specific Issues

### Windows Issues

**PowerShell Execution Policy:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Long Path Issues:**
- Enable long paths in Windows settings
- Use shorter folder names

### macOS Issues

**Permission Denied:**
```bash
chmod +x setup.sh
./setup.sh
```

**Python Version:**
```bash
# Use Python 3 explicitly
python3 gpt_creator_standalone.py config.json
```

### Linux Issues

**Missing Dependencies:**
```bash
# Ubuntu/Debian
sudo apt-get install python3-pip

# Install system dependencies
playwright install-deps
```

## 🔍 Debug Mode

Enable detailed logging by editing the script:

```python
# Change this line in gpt_creator_standalone.py
logging.basicConfig(level=logging.DEBUG)
```

This will show detailed information about what the script is doing.

## 📊 System Requirements

### Minimum Requirements
- **OS:** Windows 10, macOS 10.14, Ubuntu 18.04
- **Python:** 3.7 or higher
- **RAM:** 4GB (8GB recommended)
- **Disk:** 1GB free space
- **Internet:** Stable broadband connection

### Recommended Requirements
- **RAM:** 8GB or more
- **CPU:** Multi-core processor
- **SSD:** For faster browser startup

## 🆘 Getting Help

If none of these solutions work:

1. **Check logs:** Look for error messages in the console
2. **Test basic setup:** Try the test configuration first
3. **Update everything:** Update Python, pip, and playwright
4. **Fresh start:** Delete all generated files and start over

### Information to Include When Asking for Help

- Operating system and version
- Python version (`python --version`)
- Error messages (full text)
- Configuration file (remove sensitive data)
- Steps that led to the error

## 🔄 Starting Fresh

If all else fails, start completely fresh:

1. Delete all generated files:
   ```bash
   rm chatgpt_cookies.json
   ```

2. Reinstall dependencies:
   ```bash
   pip uninstall playwright
   pip install playwright
   playwright install chromium
   ```

3. Test with the provided example:
   ```bash
   python gpt_creator_standalone.py test-gpt-config.json
   ``` 