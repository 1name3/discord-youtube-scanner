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
            help_command=None,
        )

    async def setup_hook(self):
        """Load extensions before the bot connects."""
        await self.load_extension("bot.error_handler")
        await self.load_extension("commands.scan_command")

    async def on_ready(self):
        """Called when the bot is ready."""
        logger.info(f"✅ Bot logged in as {self.user}")
        logger.info(f"📋 Serving {len(self.guilds)} server(s)")

        for guild in self.guilds:
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)

            logger.info(
                f"🔄 Synced {len(synced)} command(s) to {guild.name}"
            )

        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="YouTube Comments",
            )
        )

    async def on_guild_join(self, guild: discord.Guild):
        """Called when the bot joins a guild."""
        logger.info(f"Joined guild: {guild.name} (ID: {guild.id})")

        self.tree.copy_global_to(guild=guild)
        synced = await self.tree.sync(guild=guild)

        logger.info(
            f"🔄 Synced {len(synced)} command(s) to {guild.name}"
        )

    async def on_error(self, event_method: str, *args, **kwargs):
        """Called when an error occurs."""
        logger.error(f"Error in {event_method}: ", exc_info=True)
