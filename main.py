"""Main entry point for the Discord YouTube Scanner bot."""

import asyncio
import sys
from bot.discord_client import DiscordBot
from config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)


async def main():
    """Main bot startup function."""
    try:
        bot = DiscordBot()

        # Load error handler
        await bot.load_extension("bot.error_handler")

        logger.info("🤖 Starting Discord YouTube Scanner Bot...")
        await bot.start(Config.DISCORD_TOKEN)

    except KeyError as e:
        logger.error(f"❌ Missing environment variable: {str(e)}")
        logger.error("Please ensure all required environment variables are set in .env file")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Failed to start bot: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
