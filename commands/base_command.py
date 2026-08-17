"""Base class for all commands."""

from abc import ABC, abstractmethod
import discord
from discord.ext import commands


class BaseCommand(commands.Cog, ABC):
    """Abstract base class for all command cogs."""

    def __init__(self, bot: commands.Bot):
        """Initialize the command.

        Args:
            bot: The Discord bot instance
        """
        self.bot = bot

    @abstractmethod
    async def setup_hooks(self):
        """Setup hooks for the command."""
        pass
