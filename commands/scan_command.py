"""Slash commands for scanning YouTube comments."""

import re
from urllib.parse import urlparse, parse_qs

import discord
from discord import app_commands
from discord.ext import commands

from scanners.keyword_scanner import KeywordScanner
from scanners.phone_scanner import PhoneScanner
from youtube.api import YouTubeAPI


# Special access control for the owner's server.
OWNER_SERVER_ID = 1413581933635440652
ALLOWED_ROLE_ID = 1539025362325995680

GITHUB_URL = "https://github.com/1name3/discord-youtube-scanner"


class ScanCommand(commands.Cog):
    """YouTube scanning commands."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.youtube = YouTubeAPI()

    scan_group = app_commands.Group(
        name="scan",
        description="Scan YouTube videos and comments.",
    )

    def has_scan_permission(self, interaction: discord.Interaction) -> bool:
        """Check whether the user is allowed to use the scanner."""

        # On every other server, everyone can use the bot.
        if interaction.guild_id != OWNER_SERVER_ID:
            return True

        # The owner's server requires the special role.
        if not isinstance(interaction.user, discord.Member):
            return False

        return any(
            role.id == ALLOWED_ROLE_ID
            for role in interaction.user.roles
        )

    async def permission_denied(
        self,
        interaction: discord.Interaction,
    ):
        """Send the permission denied message."""

        await interaction.response.send_message(
            "❌ You don't have permission to use this bot directly.\n\n"
            "📨 Please send your request in **#fih-bot-requests**.\n\n"
            "🤖 You can also build your own bot:\n"
            f"{GITHUB_URL}",
            ephemeral=True,
        )

    def extract_video_id(self, url: str):
        """Extract a YouTube video ID from a URL."""

        try:
            parsed = urlparse(url)

            # youtube.com/watch?v=VIDEO_ID
            if parsed.hostname in ("youtube.com", "www.youtube.com"):
                if parsed.path == "/watch":
                    video_id = parse_qs(parsed.query).get("v")
                    if video_id:
                        return video_id[0]

                # youtube.com/shorts/VIDEO_ID
                if parsed.path.startswith("/shorts/"):
                    return parsed.path.split("/shorts/")[1].split("/")[0]

            # youtu.be/VIDEO_ID
            if parsed.hostname == "youtu.be":
                return parsed.path.strip("/").split("/")[0]

        except Exception:
            pass

        return None

    def get_video_by_id(self, video_id: str):
        """Get a YouTube video object from an ID."""

        return self.youtube.get_video(video_id)

    async def scan_videos(
        self,
        videos,
        scanner,
    ):
        """Scan comments from a list of videos."""

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

        return results

    @scan_group.command(
        name="query",
        description="Search YouTube comments for a keyword.",
    )
    @app_commands.describe(
        query="The word or phrase to search for.",
        limit="Maximum number of videos to scan.",
        link="Optional: A specific YouTube video.",
    )
    async def scan_query(
        self,
        interaction: discord.Interaction,
        query: str,
        limit: int,
        link: str | None = None,
    ):
        """Search YouTube comments for a keyword."""

        if not self.has_scan_permission(interaction):
            await self.permission_denied(interaction)
            return

        if limit < 1 or limit > 50:
            await interaction.response.send_message(
                "❌ The limit must be between 1 and 50.",
                ephemeral=True,
            )
            return

        await interaction.response.defer()

        try:
            scanner = KeywordScanner([query])

            if link:
                video_id = self.extract_video_id(link)

                if not video_id:
                    await interaction.followup.send(
                        "❌ The provided YouTube link is invalid."
                    )
                    return

                video = self.get_video_by_id(video_id)

                if not video:
                    await interaction.followup.send(
                        "❌ The YouTube video could not be found."
                    )
                    return

                videos = [video]
                results = await self.scan_videos(videos, scanner)

            else:
                videos = self.youtube.search_videos(
                    query=query,
                    max_results=limit,
                )

                if not videos:
                    await interaction.followup.send(
                        f"🔍 No YouTube videos found for **{query}**."
                    )
                    return

                results = await self.scan_videos(videos, scanner)

            if not results:
                description = (
                    f"Search term: **{query}**\n"
                    f"📺 Videos scanned: **{len(videos)}**"
                )

                if link:
                    description += "\n🔗 Targeted video scan"

                await interaction.followup.send(
                    f"🔍 No matches found for **{query}**.\n\n"
                    f"{description}"
                )
                return

            embed = discord.Embed(
                title="🔍 YouTube Query Scan",
                description=(
                    f"Search term: **{query}**\n"
                    f"Matches: **{len(results)}**\n"
                    f"Videos: **{len(videos)}**"
                ),
                color=discord.Color.blue(),
            )

            if link:
                embed.add_field(
                    name="🔗 Mode",
                    value="Targeted video – limit was ignored.",
                    inline=False,
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
                        f"[Open comment]({comment.url})"
                    ),
                    inline=False,
                )

            if len(results) > 10:
                embed.set_footer(
                    text=f"Showing 10 of {len(results)} matches."
                )

            await interaction.followup.send(embed=embed)

        except Exception as error:
            await interaction.followup.send(
                f"❌ An error occurred while scanning:\n"
                f"`{error}`",
                ephemeral=True,
            )

    @scan_group.command(
        name="phone",
        description="Search YouTube comments for phone numbers.",
    )
    @app_commands.describe(
        limit="Maximum number of videos to scan.",
        country="Optional: Only phone numbers from this country.",
        link="Optional: A specific YouTube video.",
    )
    @app_commands.choices(
        country=[
            app_commands.Choice(name="🇦🇹 Austria (+43)", value="AT"),
            app_commands.Choice(name="🇩🇪 Germany (+49)", value="DE"),
            app_commands.Choice(name="🇨🇭 Switzerland (+41)", value="CH"),
            app_commands.Choice(name="🇬🇧 United Kingdom (+44)", value="GB"),
            app_commands.Choice(name="🇺🇸 USA/Canada (+1)", value="US/CA"),
            app_commands.Choice(name="🇫🇷 France (+33)", value="FR"),
            app_commands.Choice(name="🇮🇹 Italy (+39)", value="IT"),
            app_commands.Choice(name="🇪🇸 Spain (+34)", value="ES"),
            app_commands.Choice(name="🇳🇱 Netherlands (+31)", value="NL"),
            app_commands.Choice(name="🇧🇪 Belgium (+32)", value="BE"),
            app_commands.Choice(name="🇵🇱 Poland (+48)", value="PL"),
            app_commands.Choice(name="🇸🇪 Sweden (+46)", value="SE"),
            app_commands.Choice(name="🇳🇴 Norway (+47)", value="NO"),
            app_commands.Choice(name="🇩🇰 Denmark (+45)", value="DK"),
        ]
    )
    async def scan_phone(
        self,
        interaction: discord.Interaction,
        limit: int,
        country: app_commands.Choice[str] | None = None,
        link: str | None = None,
    ):
        """Search YouTube comments for phone numbers."""

        if not self.has_scan_permission(interaction):
            await self.permission_denied(interaction)
            return

        if limit < 1 or limit > 50:
            await interaction.response.send_message(
                "❌ The limit must be between 1 and 50.",
                ephemeral=True,
            )
            return

        await interaction.response.defer()

        try:
            country_filter = country.value if country else None
            scanner = PhoneScanner(country_filter=country_filter)

            if link:
                video_id = self.extract_video_id(link)

                if not video_id:
                    await interaction.followup.send(
                        "❌ The provided YouTube link is invalid."
                    )
                    return

                video = self.get_video_by_id(video_id)

                if not video:
                    await interaction.followup.send(
                        "❌ The YouTube video could not be found."
                    )
                    return

                videos = [video]

            else:
                videos = self.youtube.search_videos(
                    query="phone number",
                    max_results=limit,
                )

                if not videos:
                    await interaction.followup.send(
                        "🔍 No YouTube videos found."
                    )
                    return

            results = await self.scan_videos(videos, scanner)

            country_text = (
                country.name if country else "🌍 All supported countries"
            )

            if not results:
                message = (
                    "📱 No phone numbers found.\n\n"
                    f"🌍 Country: **{country_text}**\n"
                    f"📺 Videos scanned: **{len(videos)}**"
                )

                if link:
                    message += "\n🔗 Targeted video scan – limit was ignored."

                await interaction.followup.send(message)
                return

            embed = discord.Embed(
                title="📱 YouTube Phone Scan",
                description=(
                    f"Country: **{country_text}**\n"
                    f"Phone numbers: **{len(results)}**\n"
                    f"Videos: **{len(videos)}**"
                ),
                color=discord.Color.green(),
            )

            if link:
                embed.add_field(
                    name="🔗 Mode",
                    value="Targeted video – limit was ignored.",
                    inline=False,
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
                        f"🔒 Found: **{result.masked_display}**\n"
                        f"[Open comment]({comment.url})"
                    ),
                    inline=False,
                )

            if len(results) > 10:
                embed.set_footer(
                    text=f"Showing 10 of {len(results)} matches."
                )

            await interaction.followup.send(embed=embed)

        except Exception as error:
            await interaction.followup.send(
                f"❌ An error occurred while scanning:\n"
                f"`{error}`",
                ephemeral=True,
            )


async def setup(bot: commands.Bot):
    """Load the scan command."""
    await bot.add_cog(ScanCommand(bot))
