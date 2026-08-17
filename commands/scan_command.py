"""Slash command for scanning YouTube comments."""

import discord
from discord import app_commands
from discord.ext import commands

from scanners.phone_scanner import PhoneScanner
from youtube.api import YouTubeAPI


class ScanCommand(commands.Cog):
    """YouTube scanning commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.youtube = YouTubeAPI()

    @app_commands.command(
        name="scan",
        description="Scannt YouTube-Kommentare nach Telefonnummern.",
    )
    @app_commands.describe(
        query="Suchbegriff für die YouTube-Videos.",
        limit="Maximale Anzahl an Videos.",
    )
    async def scan(
        self,
        interaction: discord.Interaction,
        query: str,
        limit: int = 10,
    ):
        """Search YouTube and scan comments for phone numbers."""

        if limit < 1 or limit > 50:
            await interaction.response.send_message(
                "❌ Das Limit muss zwischen 1 und 50 liegen.",
                ephemeral=True,
            )
            return

        await interaction.response.defer()

        try:
            videos = self.youtube.search_videos(
                query=query,
                max_results=limit,
            )

            if not videos:
                await interaction.followup.send(
                    f"🔍 Keine YouTube-Videos für **{query}** gefunden."
                )
                return

            scanner = PhoneScanner()
            results = []

            for video in videos:
                comments = self.youtube.get_comments(
                    video,
                    max_results=100,
                )

                for comment in comments:
                    result = scanner.scan(comment)

                    if result:
                        results.append(result)

            if not results:
                await interaction.followup.send(
                    f"📱 Keine Telefonnummern gefunden.\n\n"
                    f"🔍 Suchbegriff: **{query}**\n"
                    f"📺 Videos durchsucht: **{len(videos)}**"
                )
                return

            embed = discord.Embed(
                title="📱 YouTube Phone Scan",
                description=(
                    f"Suchbegriff: **{query}**\n"
                    f"Telefonnummern gefunden: **{len(results)}**\n"
                    f"Videos: **{len(videos)}**"
                ),
                color=discord.Color.blue(),
            )

            for result in results[:10]:
                comment = result.comment

                text = comment.text
                if len(text) > 200:
                    text = text[:197] + "..."

                embed.add_field(
                    name=f"📱 {comment.author}",
                    value=(
                        f"{text}\n"
                        f"🔒 Gefunden: **{result.masked_display}**\n"
                        f"[Kommentar öffnen]({comment.url})"
                    ),
                    inline=False,
                )

            if len(results) > 10:
                embed.set_footer(
                    text=f"Es werden 10 von {len(results)} Treffern angezeigt."
                )

            await interaction.followup.send(embed=embed)

        except Exception as error:
            await interaction.followup.send(
                f"❌ Beim Scannen ist ein Fehler aufgetreten:\n"
                f"`{error}`",
                ephemeral=True,
            )


async def setup(bot: commands.Bot):
    """Load the scan command."""
    await bot.add_cog(ScanCommand(bot))
