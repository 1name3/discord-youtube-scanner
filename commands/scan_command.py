"""Slash commands for scanning YouTube comments."""

import discord
from discord import app_commands
from discord.ext import commands

from scanners.keyword_scanner import KeywordScanner
from scanners.phone_scanner import PhoneScanner
from youtube.api import YouTubeAPI


class ScanCommand(commands.Cog):
    """YouTube scanning commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.youtube = YouTubeAPI()

    scan_group = app_commands.Group(
        name="scan",
        description="Scannt YouTube-Videos und Kommentare.",
    )

    @scan_group.command(
        name="query",
        description="Sucht YouTube-Videos nach einem Suchbegriff.",
    )
    @app_commands.describe(
        query="Das Wort oder der Satz, nach dem gesucht werden soll.",
        limit="Maximale Anzahl an Videos.",
    )
    async def scan_query(
        self,
        interaction: discord.Interaction,
        query: str,
        limit: int = 10,
    ):
        """Search YouTube and scan comments for the given keyword."""

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

            scanner = KeywordScanner([query])
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
                    f"🔍 Keine Treffer für **{query}** gefunden.\n\n"
                    f"📺 Videos durchsucht: **{len(videos)}**"
                )
                return

            embed = discord.Embed(
                title="🔍 YouTube Query Scan",
                description=(
                    f"Suchbegriff: **{query}**\n"
                    f"Treffer: **{len(results)}**\n"
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
                    name=f"💬 {comment.author}",
                    value=(
                        f"{text}\n"
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

    @scan_group.command(
        name="phone",
        description="Sucht YouTube-Kommentare nach Telefonnummern.",
    )
    @app_commands.describe(
        country="Land der gesuchten Telefonnummern.",
        limit="Maximale Anzahl an Videos.",
    )
    @app_commands.choices(
        country=[
            app_commands.Choice(name="🇦🇹 Österreich (+43)", value="AT"),
            app_commands.Choice(name="🇩🇪 Deutschland (+49)", value="DE"),
            app_commands.Choice(name="🇨🇭 Schweiz (+41)", value="CH"),
            app_commands.Choice(name="🇬🇧 Vereinigtes Königreich (+44)", value="GB"),
            app_commands.Choice(name="🇺🇸 USA/Kanada (+1)", value="US/CA"),
            app_commands.Choice(name="🇫🇷 Frankreich (+33)", value="FR"),
            app_commands.Choice(name="🇮🇹 Italien (+39)", value="IT"),
            app_commands.Choice(name="🇪🇸 Spanien (+34)", value="ES"),
            app_commands.Choice(name="🇳🇱 Niederlande (+31)", value="NL"),
            app_commands.Choice(name="🇧🇪 Belgien (+32)", value="BE"),
            app_commands.Choice(name="🇵🇱 Polen (+48)", value="PL"),
            app_commands.Choice(name="🇸🇪 Schweden (+46)", value="SE"),
            app_commands.Choice(name="🇳🇴 Norwegen (+47)", value="NO"),
            app_commands.Choice(name="🇩🇰 Dänemark (+45)", value="DK"),
        ]
    )
    async def scan_phone(
        self,
        interaction: discord.Interaction,
        country: app_commands.Choice[str],
        limit: int = 10,
    ):
        """Search YouTube comments for phone numbers."""

        if limit < 1 or limit > 50:
            await interaction.response.send_message(
                "❌ Das Limit muss zwischen 1 und 50 liegen.",
                ephemeral=True,
            )
            return

        await interaction.response.defer()

        try:
            videos = self.youtube.search_videos(
                query=country.name,
                max_results=limit,
            )

            if not videos:
                await interaction.followup.send(
                    "🔍 Keine YouTube-Videos gefunden."
                )
                return

            scanner = PhoneScanner(country_filter=country.value)
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
                    f"📱 Keine Telefonnummern für **{country.name}** gefunden.\n\n"
                    f"📺 Videos durchsucht: **{len(videos)}**"
                )
                return

            embed = discord.Embed(
                title="📱 YouTube Phone Scan",
                description=(
                    f"Land: **{country.name}**\n"
                    f"Telefonnummern: **{len(results)}**\n"
                    f"Videos: **{len(videos)}**"
                ),
                color=discord.Color.green(),
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
