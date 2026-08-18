<div align="center">

# Fih🥀 Bot

**A powerful Python-based Discord bot that scans YouTube comments for suspicious content**

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Discord.py](https://img.shields.io/badge/discord.py-2.0%2B-blue?style=for-the-badge&logo=discord)](https://discordpy.readthedocs.io/)
[![License MIT](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![GitHub Stars](https://img.shields.io/github/stars/1name3/discord-youtube-scanner?style=for-the-badge&logo=github)](https://github.com/1name3/discord-youtube-scanner)

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Architecture](#-architecture) • [Contributing](#-contributing)

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🔍 Intelligent Scanners
- 📱 **Phone Number Detection** - 15+ countries
- 📧 **Email Detection** - Find all email addresses
- 🔎 **Keyword Scanning** - Custom pattern matching
- 🌍 **Multi-Country Support** - AT, DE, CH, GB, US, CA, FR, IT, ES, NL, BE, PL, SE, NO, DK

</td>
<td width="50%">

### 🛡️ Security & Privacy
- 🔐 **Privacy Mode** - Mask sensitive information
- 👥 **Role-Based Access** - Control who can scan
- 🔑 **Secure Tokens** - Environment-based credentials
- 📋 **Audit Logging** - Track all operations

</td>
</tr>
<tr>
<td width="50%">

### 🔧 Developer-Friendly
- 🏗️ **Modular Architecture** - Easy to extend
- 📦 **Base Classes** - Consistent implementations
- ❌ **Error Handling** - Detailed messages
- 📝 **Logging** - Track everything

</td>
<td width="50%">

### ⚡ Performance
- ⚙️ **Async/Await** - Non-blocking operations
- 💾 **Caching** - Reduce API calls
- 🚀 **Fast Scanning** - Efficient algorithms
- 📊 **Rate Limiting** - Smart quota management

</td>
</tr>
</table>

---

## 📦 Prerequisites

Before you begin, ensure you have:

| Requirement | Version | Link |
|---|---|---|
| Python | 3.9+ | [Download](https://www.python.org/downloads/) |
| Discord Bot Token | - | [Get Token](https://discord.com/developers/applications) |
| YouTube API Key | - | [Get Key](https://console.cloud.google.com/) |
| Git | Latest | [Download](https://git-scm.com/) |

---

## 🚀 Installation

### Step 1️⃣ - Clone Repository

```bash
git clone https://github.com/1name3/discord-youtube-scanner.git
cd discord-youtube-scanner
```

### Step 2️⃣ - Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3️⃣ - Setup Environment

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:
```env
# 🔑 Required
DISCORD_TOKEN=your_token_here
YOUTUBE_API_KEY=your_key_here

# ⚙️ Optional
LOG_LEVEL=INFO
BOT_PREFIX=!
PRIVACY_MODE=true
```

### Step 4️⃣ - Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5️⃣ - Start the Bot

```bash
python main.py
```

Expected output:
```
✅ Bot logged in as YourBotName#1234
📋 Serving 2 server(s)
```

---

## 🎯 Quick Start

### Add Bot to Server

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Select your application → **OAuth2 → URL Generator**
3. Select scopes: `bot`
4. Select permissions: `Send Messages`, `Embed Links`, `Read Message History`
5. Copy the URL and open in browser

### First Scan

```
/scan "python tutorial" limit:10 country:DE time_filter:7d
```

**What happens:**
1. ✅ Searches for "python tutorial" videos
2. ✅ Scans top 10 results
3. ✅ Filters to Germany, last 7 days
4. ✅ Reports suspicious content

---

## 📚 Usage Guide

### Commands

#### 🔍 `/scan` - Scan YouTube Comments

```
/scan <query> [limit] [country] [time_filter]
```

**Parameters:**
| Param | Type | Default | Range | Example |
|-------|------|---------|-------|---------|
| query | text | - | - | `"free robux"` |
| limit | number | 10 | 1-100 | `20` |
| country | text | ALL | [ISO 3166-1 alpha-2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) | `DE`, `US` |
| time_filter | text | 7d | `1h, 24h, 7d, 30d, 90d, all` | `24h` |

**Examples:**
```
/scan "cryptocurrency"
/scan "learn discord" limit:20 country:US
/scan "bitcoin" country:DE time_filter:30d
/scan "free robux" limit:5 time_filter:24h
```

#### ℹ️ `/help` - Show Help

```
/help
```

#### 📊 `/stats` - Show Statistics

```
/stats
```

---

## 🏗️ Architecture

### Project Structure

```
discord-youtube-scanner/
│
├── 📄 config.py                    ⚙️  Configuration
├── 📄 main.py                      🚀 Entry point
├── 📄 requirements.txt             📦 Dependencies
├── 📄 README.md                    📖 Documentation
│
├── 🤖 bot/
│   ├── discord_client.py          Bot setup
│   ├── error_handler.py           Error handling
│   └── __init__.py
│
├── 📺 youtube/
│   ├── models.py                  Data models
│   ├── api.py                     API wrapper
│   └── __init__.py
│
├── 🔍 scanners/
│   ├── base_scanner.py            Abstract base
│   ├── phone_scanner.py           Phone numbers
│   ├── email_scanner.py           Emails
│   ├── keyword_scanner.py         Keywords
│   └── __init__.py
│
├── ⌨️ commands/
│   ├── base_command.py            Abstract base
│   ├── scan_command.py            Scan command
│   └── __init__.py
│
├── 🎨 discord_ui/
│   ├── formatters.py              Embeds
│   └── __init__.py
│
└── 🛠️ utils/
    ├── logger.py                  Logging
    ├── validators.py              Validation
    ├── constants.py               Constants
    └── __init__.py
```

### Data Flow

```
┌─────────────────────────────────────────────────────────────┐
│                      Discord Server                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ↓
        ┌────────────────────────────────┐
        │    Discord Bot Command         │
        │   /scan <query> <params>       │
        └────────────┬───────────────────┘
                     │
                     ↓
        ┌────────────────────────────────┐
        │   Command Handler              │
        │   (Validate input)             │
        └────────────┬───────────────────┘
                     │
                     ↓
        ┌────────────────────────────────┐
        │   YouTube API Integration      │
        │   (Fetch videos & comments)    │
        └────────────┬───────────────────┘
                     │
                     ↓
        ┌────────────────────────────────┐
        │   Scanner Pipeline             │
        │   ├─ Phone Scanner             │
        │   ├─ Email Scanner             │
        │   └─ Keyword Scanner           │
        └────────────┬───────────────────┘
                     │
                     ↓
        ┌────────────────────────────────┐
        │   Result Formatter             │
        │   (Create Discord Embeds)      │
        └────────────┬───────────────────┘
                     │
                     ↓
┌─────────────────────────────────────────────────────────────┐
│              Send Results to Discord User                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 Creating Custom Scanners

### Template

**File: `scanners/custom_scanner.py`**

```python
from scanners.base_scanner import BaseScanner
from youtube.models import YouTubeComment, ScanResult
from typing import Optional
import re

class CustomScanner(BaseScanner):
    """Your scanner description here."""
    
    def __init__(self, country_filter: Optional[str] = None):
        super().__init__(country_filter)
        self.pattern = re.compile(r'your_pattern', re.IGNORECASE)
    
    def scan(self, comment: YouTubeComment) -> Optional[ScanResult]:
        """Scan comment for matches."""
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
        return True
    
    def get_supported_countries(self) -> list:
        """Get supported countries."""
        return []
```

### Registration

```python
from scanners.custom_scanner import CustomScanner

scanner = CustomScanner()
result = scanner.scan(comment)
```

---

## ⚙️ Configuration

### Environment Variables

```env
# 🔐 Required
DISCORD_TOKEN=your_discord_bot_token_here
YOUTUBE_API_KEY=your_youtube_api_key_here

# ⚙️ Optional
LOG_LEVEL=INFO                    # DEBUG, INFO, WARNING, ERROR
BOT_PREFIX=!                      # Command prefix
PRIVACY_MODE=true                 # Mask sensitive data
```

### Bot Settings (config.py)

```python
class Config:
    # Bot
    BOT_PREFIX = "!"
    PRIVACY_MODE = True
    
    # YouTube API
    YOUTUBE_MAX_RESULTS = 100
    YOUTUBE_TIMEOUT = 30
    
    # Scanners
    CONFIDENCE_THRESHOLD = 0.7
    MAX_COMMENTS_PER_VIDEO = 1000
```

---

## 📊 Output Examples

### Single Result
```
🔍 PHONE DETECTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Author: john_doe
"Looking for roommates, call +43 660 123456"

Confidence: 92%
Video: How to find apartments in Vienna
```

### Scan Summary
```
📊 SCAN RESULTS: 5 Matches Found
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 Phone Numbers:    3 matches
📧 Emails:          2 matches
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Time: 2.3s
Videos Scanned: 10
```

---

## 🐛 Troubleshooting

### ❌ Bot won't start

```
❌ Missing environment variable: DISCORD_TOKEN
```

**Solution:**
- Create `.env` file in project root
- Add all required tokens
- Verify file is in correct location

### ⚠️ API rate limit exceeded

```
⚠️ YouTube API quota exceeded
```

**Solution:**
- Check quota at [Google Cloud Console](https://console.cloud.google.com/)
- Free tier: 10,000 units/day
- Upgrade plan if needed

### 🔍 No results found

**Solution:**
- Try different search query
- Verify YouTube API key is valid
- Check remaining API quota

### 🚫 Permission denied

```
MissingPermissions: Missing required permissions
```

**Solution:**
- Go to Server Settings → Roles → Select Bot Role
- Enable: `Send Messages`, `Embed Links`, `Read Message History`

---

## 🤝 Contributing

### 1️⃣ Fork Repository
Click "Fork" on GitHub

### 2️⃣ Create Feature Branch
```bash
git checkout -b feature/amazing-feature
```

### 3️⃣ Make Changes
```bash
# Write clean code
# Add docstrings
# Follow code style
```

### 4️⃣ Commit
```bash
git commit -m "Add feature: description"
```

### 5️⃣ Push
```bash
git push origin feature/amazing-feature
```

### 6️⃣ Create Pull Request
Describe your changes clearly

### Code Style

- ✅ Use `snake_case` for variables
- ✅ Use `PascalCase` for classes
- ✅ Add type hints
- ✅ Max line length: 100 chars
- ✅ Write docstrings

---

## 📄 License

This project is licensed under the **MIT License**

```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

See [LICENSE](LICENSE) for full text.

---

## 📞 Support

### Get Help

| Channel | Link |
|---------|------|
| 📝 Issues | [Open Issue](https://github.com/1name3/discord-youtube-scanner/issues) |
| 💬 Discussions | [Start Discussion](https://github.com/1name3/discord-youtube-scanner/discussions) |

---

## ⚖️ Legal Disclaimer

This project is provided **"AS IS"** without warranty. Users are responsible for:

- ✅ Complying with YouTube Terms of Service
- ✅ Respecting privacy laws and regulations
- ✅ Using the bot ethically and responsibly
- ✅ Following Discord Community Guidelines

---

## 📈 Roadmap

- [ ] 📱 Phone number scanner
- [ ] 📧 Email scanner
- [ ] 🔑 Keyword scanner
- [ ] 💾 Database storage
- [ ] 🌐 Web dashboard
- [ ] 🔌 Webhook integrations
- [ ] 🌍 Multi-language support
- [ ] ⚡ Performance optimizations

---

<div align="center">

### ⭐ Found this helpful? Star us on GitHub!

[⬆ Back to Top](#-discord-youtube-scanner-bot)

**[Issues](https://github.com/1name3/discord-youtube-scanner/issues)** • **[Discussions](https://github.com/1name3/discord-youtube-scanner/discussions)** • **[Contact](mailto:simon.manigatterer33@gmail.com)**

</div>
