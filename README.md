````markdown name=README.md
# Discord YouTube Scanner Bot

Ein Python-basierter Discord-Bot, der YouTube-Kommentare auf verdächtige Inhalte wie Telefonnummern, E-Mail-Adressen und mehr scannt.

## Features

✨ **Intelligente Scanner:**
- 📱 **Telefonnummern Scanner** - Erkennt Telefonnummern aus verschiedenen Ländern
- 📧 **E-Mail Scanner** - Findet E-Mail-Adressen in Kommentaren
- 🔍 **Keyword Scanner** - Sucht nach benutzerdefinierten Stichwörtern
- 🌍 **Multi-Land-Unterstützung** - Unterstützt 15+ Länder

🛡️ **Sicherheit:**
- Privacy-Mode: Maskiert gefundene Inhalte in Ausgaben
- Rollenbasierte Zugriffskontrolle
- Sichere Token-Verwaltung über .env

🔧 **Developer-freundlich:**
- Modulare Architektur mit Base-Klassen
- Einfache Erweiterung durch neue Scanner
- Comprehensive Error Handling
- Detaillierte Logging

## Installation

### Voraussetzungen
- Python 3.9+
- Discord Bot Token (von [Discord Developer Portal](https://discord.com/developers/applications))
- YouTube API Key (von [Google Cloud Console](https://console.cloud.google.com))

### Setup

1. **Repository klonen:**
```bash
git clone https://github.com/1name3/discord-youtube-scanner.git
cd discord-youtube-scanner
```

2. **Virtual Environment erstellen:**
```bash
python -m venv venv
source venv/bin/activate  # Unter Windows: venv\Scripts\activate
```

3. **.env Datei erstellen:**
```bash
cp .env.example .env
```

4. **.env mit deinen Daten füllen:**
```env
DISCORD_TOKEN=your_discord_bot_token
YOUTUBE_API_KEY=your_youtube_api_key
LOG_LEVEL=INFO
```

5. **Dependencies installieren:**
```bash
pip install -r requirements.txt
```

6. **Bot starten:**
```bash
python main.py
```

## Verwendung

### Befehle

```
/scan <query> [limit] [country] [time_filter]
  - Sucht nach Videos mit der Query
  - limit: Anzahl der zu scannenden Videos (1-100)
  - country: Länderfilter (z.B. AT, DE, CH)
  - time_filter: Zeitfilter (1h, 24h, 7d, 30d, 90d, all)

/help
  - Zeigt alle verfügbaren Befehle
```

### Beispiele

```
/scan "python tutorial" limit:10 country:DE time_filter:7d
/scan "discord bot" limit:5
```

## Architektur

```
discord-youtube-scanner/
├── bot/                      # Discord Bot Setup
│   ├── discord_client.py     # Bot-Initialisierung
│   └── error_handler.py      # Error Handling
├── youtube/                  # YouTube API Integration
│   └── models.py            # Data Models
├── scanners/                 # Scanner Implementierungen
│   ├── base_scanner.py       # Abstract Base Class
│   ├── phone_scanner.py      # Phone Number Scanner
│   ├── email_scanner.py      # Email Scanner
│   └── keyword_scanner.py    # Keyword Scanner
├── commands/                 # Discord Commands
│   ├── base_command.py       # Abstract Command Class
│   └── scan_command.py       # Scan Command
├── discord_ui/               # UI Formatters
│   └── formatters.py        # Discord Embed Formatters
├── utils/                    # Utility Functions
│   ├── logger.py            # Logging Setup
│   ├── validators.py        # Input Validation
│   └── constants.py         # Constants & Messages
├── config.py                # Configuration
├── main.py                  # Entry Point
└── requirements.txt         # Dependencies
```

## Konfiguration

Alle Einstellungen können über die `config.py` Datei angepasst werden:

```python
class Config:
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    BOT_PREFIX = "!"
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    # ... weitere Einstellungen
```

## Einen neuen Scanner hinzufügen

1. Neue Datei erstellen `scanners/custom_scanner.py`
2. Von `BaseScanner` erben:

```python
from scanners.base_scanner import BaseScanner
from youtube.models import YouTubeComment, ScanResult

class CustomScanner(BaseScanner):
    def scan(self, comment: YouTubeComment) -> Optional[ScanResult]:
        # Implementierung
        pass
    
    def supports_country(self, country_code: str) -> bool:
        # Implementierung
        pass
```

3. Scanner in Command registrieren

## Beiträge

Contributions sind willkommen! Bitte:

1. Fork das Projekt
2. Feature Branch erstellen (`git checkout -b feature/AmazingFeature`)
3. Änderungen committen (`git commit -m 'Add AmazingFeature'`)
4. Branch pushen (`git push origin feature/AmazingFeature`)
5. Pull Request öffnen

## Lizenz

Dieses Projekt ist unter der MIT Lizenz lizenziert - siehe [LICENSE](LICENSE) Datei für Details.

## Support

Bei Fragen oder Problemen:
- 📝 [Issues](https://github.com/1name3/discord-youtube-scanner/issues) öffnen
- 💬 Discussions nutzen
- 📧 Kontakt: simon.manigatterer33@gmail.com

## Disclaimer

Dieses Projekt wird bereitgestellt "AS IS" ohne Garantien. Benutzer sind verantwortlich für die Einhaltung aller geltenden Gesetze und Richtlinien bei der Nutzung dieses Bots.

---

Made with ❤️ by [1name3](https://github.com/1name3)
````
