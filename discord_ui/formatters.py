"""Discord UI formatters for displaying scan results."""

import discord
from typing import List
from youtube.models import ScanResult, YouTubeComment
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ResultFormatter:
    """Formats scan results for Discord display."""

    @staticmethod
    def format_single_result(result: ScanResult) -> discord.Embed:
        """Format a single scan result as a Discord embed.

        Args:
            result: The scan result to format

        Returns:
            discord.Embed: Formatted embed
        """
        embed = discord.Embed(
            title=f"🔍 {result.scanner_type.upper()} Treffer",
            description=result.masked_display,
            color=discord.Color.red() if result.confidence > 0.8 else discord.Color.orange(),
        )

        embed.add_field(
            name="Kommentar",
            value=f"Von: {result.comment.author}\n{result.comment.text[:200]}...",
            inline=False,
        )

        embed.add_field(
            name="Zuversicht",
            value=f"{result.confidence * 100:.0f}%",
            inline=True,
        )

        embed.add_field(
            name="Video",
            value=f"[{result.comment.video_title}]({result.comment.url})",
            inline=False,
        )

        embed.timestamp = result.comment.published_at

        return embed

    @staticmethod
    def format_results_summary(results: List[ScanResult]) -> discord.Embed:
        """Format multiple results as a summary embed.

        Args:
            results: List of scan results

        Returns:
            discord.Embed: Summary embed
        """
        if not results:
            return discord.Embed(
                title="Keine Treffer",
                description="Die Suche hat keine Ergebnisse gefunden.",
                color=discord.Color.green(),
            )

        embed = discord.Embed(
            title=f"📊 Zusammenfassung: {len(results)} Treffer",
            color=discord.Color.red() if len(results) > 5 else discord.Color.orange(),
        )

        scanner_counts = {}
        for result in results:
            scanner_counts[result.scanner_type] = scanner_counts.get(result.scanner_type, 0) + 1

        for scanner_type, count in scanner_counts.items():
            embed.add_field(
                name=scanner_type.upper(),
                value=f"{count} Treffer",
                inline=True,
            )

        return embed
