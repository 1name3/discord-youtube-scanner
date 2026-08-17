"""Centralized error handling for the Discord bot."""

import discord
from discord.ext import commands
from utils.logger import setup_logger
from utils.constants import ERROR_MESSAGES

logger = setup_logger(__name__)


class BotErrorHandler(commands.Cog):
    """Global error handler for bot commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        """Handle command errors.

        Args:
            ctx: Command context
            error: The error that occurred
        """
        logger.error(f"Command error in {ctx.command}: {str(error)}")

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f"Fehlendes Argument: {error.param.name}\n"
                f"Verwenden Sie `/help` für mehr Informationen.",
                ephemeral=True,
            )
        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                f"Ungültiges Argument: {str(error)}",
                ephemeral=True,
            )
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send(
                "Befehl nicht gefunden.\n"
                "Verwenden Sie `/help` für eine Liste verfügbarer Befehle.",
                ephemeral=True,
            )
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "Sie haben keine Berechtigung für diesen Befehl.",
                ephemeral=True,
            )
        else:
            await ctx.send(
                f"Ein Fehler ist aufgetreten: {str(error)}",
                ephemeral=True,
            )


async def setup(bot: commands.Bot):
    """Setup error handler cog.

    Args:
        bot: The Discord bot instance
    """
    await bot.add_cog(BotErrorHandler(bot))
