````markdown name=README.md
# Discord YouTube Scanner Bot

A powerful Python-based Discord bot that scans YouTube comments for suspicious content including phone numbers, email addresses, and custom keywords.

## ✨ Features

### 🔍 Intelligent Scanners
- **📱 Phone Number Scanner** - Detects phone numbers from 15+ countries
- **📧 Email Scanner** - Identifies email addresses in comments
- **🔎 Keyword Scanner** - Searches for custom keywords and phrases
- **🌍 Multi-Country Support** - Supports AT, DE, CH, GB, US, CA, FR, IT, ES, NL, BE, PL, SE, NO, DK and more

### 🛡️ Security & Privacy
- **Privacy Mode** - Masks sensitive information in outputs
- **Role-Based Access Control** - Configure who can use the bot
- **Secure Token Management** - Credentials stored in `.env` file
- **Audit Logging** - Track all scan operations

### 🔧 Developer-Friendly
- **Modular Architecture** - Easy to extend with new scanners
- **Base Classes** - Abstract base classes for consistent implementation
- **Comprehensive Error Handling** - Detailed error messages and recovery
- **Detailed Logging** - Track bot operations and issues

---

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage](#usage)
- [Architecture](#architecture)
- [Adding Custom Scanners](#adding-custom-scanners)
- [Contributing](#contributing)
- [License](#license)

---

## 🚀 Installation

### Prerequisites

- **Python 3.9+** - [Download here](https://www.python.org/downloads/)
- **Discord Bot Token** - Get it from [Discord Developer Portal](https://discord.com/developers/applications)
- **YouTube API Key** - Get it from [Google Cloud Console](https://console.cloud.google.com/)
- **Git** - [Download here](https://git-scm.com/)

### Step-by-Step Setup

**1. Clone the Repository**
```bash
git clone https://github.com/1name3/discord-youtube-scanner.git
cd discord-youtube-scanner
```

**2. Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Create Environment Configuration**
```bash
cp .env.example .env
```

**4. Configure Environment Variables**

Edit `.env` and add your credentials:
```env
# Required
DISCORD_TOKEN=your_discord_bot_token_here
YOUTUBE_API_KEY=your_youtube_api_key_here

# Optional
LOG_LEVEL=INFO
BOT_PREFIX=!
PRIVACY_MODE=true
```

**5. Install Dependencies**
```bash
pip install -r requirements.txt
```

**6. Run the Bot**
```bash
python main.py
```

You should see:
```
✅ Bot logged in as YourBotName#1234
📋 Serving 2 server(s)
```

---

## 🎯 Quick Start

### Adding the Bot to Your Server

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your application
3. Go to **OAuth2 → URL Generator**
4. Select scopes: `bot`
5. Select permissions: `Send Messages`, `Embed Links`, `Read Message History`
6. Copy the generated URL and open it in your browser

### First Scan

Once the bot is running and added to your server:

```
/scan "python tutorial" limit:10 country:DE time_filter:7d
```

The bot will:
1. Search for YouTube videos matching "python tutorial"
2. Scan comments from the top 10 results
3. Filter to videos from Germany posted in the last 7 days
4. Report any suspicious content found

---

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DISCORD_TOKEN` | ✅ Yes | - | Your Discord bot token |
| `YOUTUBE_API_KEY` | ✅ Yes | - | Your YouTube API key |
| `LOG_LEVEL` | ❌ No | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `BOT_PREFIX` | ❌ No | `!` | Command prefix for text commands |
| `PRIVACY_MODE` | ❌ No | `true` | Mask sensitive data in outputs |

### Bot Configuration

Edit `config.py` to customize bot behavior:

```python
class Config:
    # Bot Settings
    BOT_PREFIX = "!"
    PRIVACY_MODE = True
    
    # API Settings
    YOUTUBE_MAX_RESULTS = 100
    YOUTUBE_TIMEOUT = 30
    
    # Scanner Settings
    CONFIDENCE_THRESHOLD = 0.7
    MAX_COMMENTS_PER_VIDEO = 1000
```

---

## 💬 Usage

### Available Commands

#### `/scan`
Search YouTube and scan comments for suspicious content.

**Syntax:**
```
/scan <query> [limit] [country] [time_filter]
```

**Parameters:**
- `query` *(required)* - Search term or phrase
- `limit` *(optional)* - Number of videos to scan (1-100, default: 10)
- `country` *(optional)* - Country code filter (AT, DE, CH, etc., default: ALL)
- `time_filter` *(optional)* - Time range (1h, 24h, 7d, 30d, 90d, all, default: 7d)

**Examples:**
```
/scan "cryptocurrency"
/scan "learn discord" limit:20 country:US
/scan "free robux" limit:5 time_filter:24h
/scan "bitcoin" country:DE time_filter:30d
```

#### `/help`
Display help information and available commands.

```
/help
```

#### `/stats`
Show statistics about recent scans.

```
/stats
```

---

## 🏗️ Architecture

### Project Structure

```
discord-youtube-scanner/
│
├── 📄 config.py                    # Configuration and settings
├── 📄 main.py                      # Application entry point
├── 📄 requirements.txt             # Python dependencies
├── 📄 README.md                    # Documentation (you are here)
│
├── 🤖 bot/
│   ├── discord_client.py          # Bot initialization and setup
│   ├── error_handler.py           # Global error handling
│   └── __init__.py
│
├── 📺 youtube/
│   ├── models.py                  # Data models (Video, Comment, etc.)
│   ├── api.py                     # YouTube API wrapper (to implement)
│   └── __init__.py
│
├── 🔍 scanners/
│   ├── base_scanner.py            # Abstract scanner base class
│   ├── phone_scanner.py           # Phone number detection (to implement)
│   ├── email_scanner.py           # Email detection (to implement)
│   ├── keyword_scanner.py         # Keyword detection (to implement)
│   └── __init__.py
│
├── ⌨️ commands/
│   ├── base_command.py            # Abstract command base class
│   ├── scan_command.py            # Main scan command (to implement)
│   ├── help_command.py            # Help command (to implement)
│   └── __init__.py
│
├── 🎨 discord_ui/
│   ├── formatters.py              # Discord embed formatters
│   └── __init__.py
│
└── 🛠️ utils/
    ├── logger.py                  # Logging configuration
    ├── validators.py              # Input validation utilities
    ├── constants.py               # Constants and static data
    └── __init__.py
```

### Architecture Diagram

```
Discord Server
      ↓
┌─────────────────┐
│  Discord Bot    │
│  (discord_client)
└────────┬────────┘
         ↓
┌─────────────────────────┐
│   Command Handler       │
│  (base_command.py)      │
└────────┬────────────────┘
         ↓
┌──────────────────��──────┐
│  YouTube API Integration│
│  (youtube/api.py)       │
└────────┬────────────────┘
         ↓
┌─────────────────────────┐
│  Scanner Pipeline       │
│  (scanners/)            │
│  ├─ Phone Scanner       │
│  ├─ Email Scanner       │
│  └─ Keyword Scanner     │
└────────┬────────────────┘
         ↓
┌─────────────────────────┐
│  Result Formatting      │
│  (discord_ui/)          │
└────────┬────────────────┘
         ↓
    Discord User
```

---

## 🔧 Adding Custom Scanners

Creating a custom scanner is simple and follows a consistent pattern.

### Example: Creating a Custom Scanner

**File: `scanners/custom_scanner.py`**

```python
from scanners.base_scanner import BaseScanner
from youtube.models import YouTubeComment, ScanResult
from typing import Optional
import re

class CustomScanner(BaseScanner):
    """Detect custom suspicious patterns."""
    
    def __init__(self, country_filter: Optional[str] = None):
        super().__init__(country_filter)
        self.pattern = re.compile(r'your_pattern_here', re.IGNORECASE)
    
    def scan(self, comment: YouTubeComment) -> Optional[ScanResult]:
        """Scan a comment for suspicious content."""
        matches = self.pattern.findall(comment.text)
        
        if not matches:
            return None
        
        return ScanResult(
            comment=comment,
            scanner_type=self.scanner_type,
            matches={"found": matches},
            confidence=0.95,
            masked_display=f"Found {len(matches)} match(es)"
        )
    
    def supports_country(self, country_code: str) -> bool:
        """Check if scanner supports country."""
        return True  # Supported everywhere
    
    def get_supported_countries(self) -> list:
        """Get supported countries."""
        return []  # All countries
```

### Key Methods to Implement

| Method | Purpose | Returns |
|--------|---------|---------|
| `scan()` | Analyze comment for matches | `ScanResult` or `None` |
| `supports_country()` | Check country support | `bool` |
| `get_supported_countries()` | List supported countries | `list` |

### Registering Your Scanner

In your command handler:

```python
from scanners.custom_scanner import CustomScanner

scanner = CustomScanner()
result = scanner.scan(comment)
```

---

## 📊 Output Examples

### Successful Scan
```
🔍 PHONE TREFFER
Kommentar
Von: john_doe
Looking for roommates, call me at +43 660 123456

Zuversicht
92%

Video
[How to find apartments in Vienna](https://youtube.com/watch?v=...)
```

### Scan Summary
```
📊 Zusammenfassung: 5 Treffer
PHONE: 3 Treffer
EMAIL: 2 Treffer
```

---

## 🤝 Contributing

We welcome contributions! Here's how to help:

### 1. Fork the Repository
Click the "Fork" button on GitHub

### 2. Create a Feature Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Make Your Changes
- Write clean, documented code
- Follow the existing code style
- Add docstrings to functions

### 4. Commit Your Changes
```bash
git commit -m "Add feature: description of your changes"
```

### 5. Push to Your Fork
```bash
git push origin feature/your-feature-name
```

### 6. Create a Pull Request
- Go to the original repository
- Click "New Pull Request"
- Describe your changes clearly

### Code Style Guidelines

- Use **snake_case** for variables and functions
- Use **PascalCase** for classes
- Add type hints where possible
- Maximum line length: 100 characters
- Write clear docstrings for all functions

---

## 🐛 Troubleshooting

### Bot won't start
```
❌ Missing environment variable: DISCORD_TOKEN
```
**Solution:** Ensure `.env` file exists and contains `DISCORD_TOKEN`

### API rate limit exceeded
```
⚠️ YouTube API quota exceeded
```
**Solution:** Check your API quota at [Google Cloud Console](https://console.cloud.google.com/). Free tier has 10,000 units/day.

### No results found
```
Keine Ergebnisse gefunden
```
**Solution:** 
- Try a different search query
- Check that your YouTube API key is valid
- Ensure you have API quota remaining

### Permission denied errors
```
MissingPermissions: Missing required permissions
```
**Solution:** Check bot permissions in Discord server settings. Bot needs: `Send Messages`, `Embed Links`, `Read Message History`

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### What this means:
- ✅ You can use it for commercial projects
- ✅ You can modify the code
- ✅ You can distribute it
- ⚠️ You must include the license and copyright notice

---

## 📞 Support & Contact

### Get Help

- 📝 **Issues:** [Open an issue](https://github.com/1name3/discord-youtube-scanner/issues)
- 💬 **Discussions:** [Start a discussion](https://github.com/1name3/discord-youtube-scanner/discussions)
- 📧 **Email:** simon.manigatterer33@gmail.com
- 🐦 **Twitter:** [@1name3](https://twitter.com/1name3)

### Report a Security Issue

Please **DO NOT** open a public issue for security vulnerabilities. Instead, email us directly.

---

## ⚖️ Legal Disclaimer

This project is provided "AS IS" without any warranty. Users are responsible for:
- Complying with YouTube's Terms of Service
- Respecting privacy laws and regulations
- Using the bot ethically and responsibly
- Following Discord's Community Guidelines

---

## 🎉 Credits

**Created with ❤️ by [1name3](https://github.com/1name3)**

### Technologies Used
- [discord.py](https://discordpy.readthedocs.io/) - Discord API wrapper
- [google-api-python-client](https://github.com/googleapis/google-api-python-client) - YouTube API client
- [python-dotenv](https://github.com/theskumar/python-dotenv) - Environment management

---

## 📈 Roadmap

- [ ] Phone number scanner implementation
- [ ] Email scanner implementation
- [ ] Keyword scanner implementation
- [ ] Database for storing scan results
- [ ] Web dashboard for statistics
- [ ] Advanced filtering options
- [ ] Webhook integrations
- [ ] Multi-language support

---

<div align="center">

**[⬆ back to top](#discord-youtube-scanner-bot)**

Made with 💜 for the Discord community

</div>
````
