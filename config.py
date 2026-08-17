"""Configuration module for Discord YouTube Scanner Bot.

Loads environment variables from .env file and provides configuration
across the application.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)


class Config:
    """Main configuration class."""

    # Discord Bot Configuration
    DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
    BOT_PREFIX = os.getenv("BOT_PREFIX", "/")
    BOT_LANGUAGE = os.getenv("BOT_LANGUAGE", "de")

    # YouTube API Configuration
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
    YOUTUBE_API_VERSION = "v3"
    YOUTUBE_MAX_RESULTS_PER_SEARCH = 20  # Videos per search (limited for quota)
    YOUTUBE_MAX_COMMENTS_PER_VIDEO = 100  # Comments per video
    YOUTUBE_DAILY_QUOTA_LIMIT = 10000

    # Logging Configuration
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Development Configuration
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

    # Search Limits
    MAX_SEARCH_RESULTS_PER_PAGE = 5
    MAX_PAGES = 50  # Prevent infinite pagination
    RESULT_CACHE_TTL_SECONDS = 3600  # 1 hour cache

    # Phone Scanner Configuration
    PHONE_SCANNER_ENABLED = True
    PHONE_MASK_CHAR = "X"
    PHONE_MIN_CONFIDENCE = 0.7  # 0.0-1.0

    # UI Configuration
    EMBED_COLOR_SUCCESS = 0x00FF00  # Green
    EMBED_COLOR_INFO = 0x0099FF  # Blue
    EMBED_COLOR_WARNING = 0xFFAA00  # Orange
    EMBED_COLOR_ERROR = 0xFF0000  # Red
    BUTTON_TIMEOUT_SECONDS = 300  # 5 minutes

    # Privacy Configuration
    STORE_FULL_PHONE_NUMBERS = False  # NEVER store full numbers
    LOG_SENSITIVE_DATA = False  # NEVER log phone numbers

    @classmethod
    def validate(cls) -> bool:
        """Validate that all required configuration values are present.

        Returns:
            bool: True if configuration is valid, False otherwise.
        """
        required_vars = [
            "DISCORD_TOKEN",
            "YOUTUBE_API_KEY",
        ]

        missing_vars = [var for var in required_vars if not getattr(cls, var)]

        if missing_vars:
            print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
            print(f"   Please create a .env file with these variables.")
            print(f"   See .env.example for reference.")
            return False

        print("✅ Configuration validated successfully.")
        return True
