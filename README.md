# GPT Builder Script

An automated Python script that creates and updates custom GPTs on OpenAI's ChatGPT platform using browser automation. This script can configure GPT settings, add conversation starters, and integrate custom APIs through OpenAPI specifications.

## 🚀 Features

- **Automated GPT Creation**: Create new custom GPTs programmatically
- **GPT Updates**: Update existing GPTs with new configurations
- **API Integration**: Add custom actions via OpenAPI specifications
- **Conversation Starters**: Automatically configure conversation starters
- **Session Management**: Saves login cookies for faster subsequent runs
- **Error Recovery**: Robust error handling with automatic retries
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 📋 Prerequisites

- Python 3.7 or higher
- Active OpenAI ChatGPT Plus subscription (required for custom GPTs)
- Internet connection

## 🛠️ Installation

### 1. Clone or Download the Repository

```bash
git clone <repository-url>
cd GPTBuilder
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Playwright Browsers

After installing the Python packages, you need to install the browser binaries to the correct path:

**Using Setup Scripts (Recommended - Run Once):**
```bash
# Windows
setup.bat

# macOS/Linux  
chmod +x setup.sh
./setup.sh
```

> **Note:** You only need to run the setup script once. After that, you can run the Python script directly - it automatically handles the browser path configuration.

**Manual Installation:**
```bash
# Set browser path to match script requirements
set PLAYWRIGHT_BROWSERS_PATH=%USERPROFILE%\.playwright-browsers     # Windows
export PLAYWRIGHT_BROWSERS_PATH="$HOME/.playwright-browsers"        # macOS/Linux

# Install browsers
python -m playwright install chromium --with-deps
```

## 📁 Project Structure

```
GPTBuilder/
├── gpt_creator_standalone.py    # Main script
├── requirements.txt             # Python dependencies
├── test-gpt-config.json        # Example GPT configuration
├── test_openapi.json           # Example OpenAPI specification
├── README.md                   # This file
└── chatgpt_cookies.json        # Auto-generated (login session data)
```

## ⚙️ Configuration

### GPT Configuration File

Create a JSON configuration file for your GPT. Use `test-gpt-config.json` as a template:

```json
{
  "name": "Your GPT Name",
  "description": "Description of what your GPT does",
  "instructions": "Detailed instructions for your GPT's behavior",
  "conversation_starters": [
    "What can you help me with?",
    "How do you work?",
    "Tell me about your features"
  ],
  "openapi_spec_file": "your_openapi.json"
}
```

#### Configuration Fields:

- **name** (required): The name of your GPT
- **description** (required): Brief description shown in the GPT store
- **instructions** (required): Detailed instructions that define your GPT's behavior
- **conversation_starters** (optional): Array of suggested conversation starters
- **openapi_spec_file** (optional): Path to OpenAPI specification file for custom actions

### OpenAPI Specification (Optional)

If your GPT needs to call external APIs, create an OpenAPI 3.1.0 specification file. Use `test_openapi.json` as a template:

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "Your API",
    "description": "Description of your API",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "https://your-api-domain.com",
      "description": "Your API server"
    }
  ],
  "paths": {
    "/your-endpoint": {
      "get": {
        "operationId": "your_operation",
        "summary": "What this endpoint does",
        "parameters": [
          {
            "name": "param_name",
            "in": "query",
            "required": true,
            "schema": {
              "type": "string"
            }
          }
        ],
        "responses": {
          "200": {
            "description": "Successful response"
          }
        }
      }
    }
  }
}
```

## 🚀 Usage

### Basic Usage

```bash
python gpt_creator_standalone.py your-config.json
```

### Example with Test Configuration

```bash
python gpt_creator_standalone.py test-gpt-config.json
```

### Typical Workflow

1. **First time:** Run setup script (`setup.bat` or `./setup.sh`)
2. **Every time after:** Just run the Python script directly
   ```bash
   python gpt_creator_standalone.py your-config.json
   ```

The script automatically handles browser path configuration, so you don't need to run setup again.

## 📝 Step-by-Step Process

1. **Browser Launch**: The script opens a Chrome browser window
2. **Login**: Navigate to ChatGPT and log in manually when prompted
3. **GPT Detection**: Checks if a GPT with the same name already exists
4. **GPT Creation/Update**: Creates new GPT or updates existing one
5. **Configuration**: Sets name, description, and instructions
6. **Conversation Starters**: Adds suggested conversation starters
7. **API Integration**: Configures custom actions if OpenAPI spec provided
8. **Save & Publish**: Saves the GPT with "Only me" privacy setting

## 🔐 Authentication

### First Run
- The script will open a browser window
- Navigate to ChatGPT and log in manually
- Your login session will be saved for future runs

### Subsequent Runs
- The script will automatically use saved cookies
- Manual login only required if session expires

## 🛡️ Privacy & Security

- GPTs are created with "Only me" privacy setting by default
- Login cookies are stored locally in `chatgpt_cookies.json`
- No sensitive data is transmitted to third parties
- Browser automation uses human-like patterns to avoid detection

## 🔧 Troubleshooting

### Common Issues

**"Browser crashed" errors:**
- The script automatically retries up to 3 times
- Ensure you have sufficient system memory
- Close other browser instances before running

**Login issues:**
- Delete `chatgpt_cookies.json` and try again
- Ensure you have an active ChatGPT Plus subscription
- Check your internet connection

**CAPTCHA challenges:**
- Complete the "Verify you are human" challenge manually
- The script will continue automatically after verification
- This is normal behavior for automated browsers

**"GPT creation failed" errors:**
- Verify your configuration JSON is valid
- Ensure all required fields are present
- Check that OpenAPI specification is valid (if provided)

**Playwright installation issues:**
```bash
# Reinstall playwright browsers
playwright install --force chromium
```

### Debug Mode

For detailed logging, modify the logging level in the script:
```python
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Supported Configurations

### GPT Settings
- ✅ Name and description
- ✅ Custom instructions
- ✅ Conversation starters
- ✅ Custom actions (via OpenAPI)
- ✅ Privacy settings

### API Integration
- ✅ OpenAPI 3.1.0 specifications
- ✅ GET, POST, PUT, DELETE methods
- ✅ Query parameters
- ✅ Request/response schemas
- ✅ Authentication headers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is provided as-is for educational and personal use. Please respect OpenAI's terms of service when using this script.

## ⚠️ Disclaimer

- This script uses browser automation and may break if OpenAI changes their interface
- Use responsibly and in accordance with OpenAI's terms of service
- The script is provided without warranty
- Always test with non-critical GPTs first

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Ensure all dependencies are correctly installed
3. Verify your configuration files are valid JSON
4. Try running with a fresh browser session (delete cookies file)

For additional help, please create an issue in the repository with:
- Your operating system
- Python version
- Error messages (if any)
- Configuration file (remove sensitive data) 