"""Discord bot client setup and initialization."""

import discord
from discord.ext import commands
from config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class DiscordBot(commands.Bot):
    """Custom Discord bot class."""

    def __init__(self):
        """Initialize the Discord bot."""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True

        super().__init__(
            command_prefix=Config.BOT_PREFIX,
            intents=intents,
            help_command=None,  # We'll use slash commands
        )

    async def on_ready(self):
        """Called when the bot is ready."""
        logger.info(f"✅ Bot logged in as {self.user}")
        logger.info(f"📋 Serving {len(self.guilds)} server(s)")

        try:
            synced = await self.tree.sync()
            logger.info(f"🔄 Synced {len(synced)} slash command(s)")
        except Exception as e:
            logger.error(f"❌ Failed to sync slash commands: {e}")

        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="YouTube Comments",
            )
        )

    async def on_guild_join(self, guild: discord.Guild):
        """Called when the bot joins a guild.

        Args:
            guild: The guild that was joined
        """
        logger.info(f"Joined guild: {guild.name} (ID: {guild.id})")

    async def on_error(self, event_method: str, *args, **kwargs):
        """Called when an error occurs.

        Args:
            event_method: The name of the event method
            *args: Positional arguments
            **kwargs: Keyword arguments
        """
        logger.error(f"Error in {event_method}: ", exc_info=True)
