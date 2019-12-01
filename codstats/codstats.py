import discord
import aiohttp
from redbot.core import commands, checks, Config
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from redbot.core.utils.chat_formatting import pagify

class CODSTATS(commands.Cog):
    """"Simple Commands to get stats for COD"""

    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, identifier=6991142013)

        self._session = aiohttp.ClientSession()

    def cog_unload(self):
        self.bot.loop.create_task(self._session.close())

    @commands.command()
    async def codstats(self, ctx, platform, username):
        """Command to get your COD: MW stats"""
        embeds = []
        platform = platform.replace("pc", "battle")
        username = username.replace("#", "%23")
        async with self._session.get(
                f"https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/{platform}/gamer/{username}/profile/type/mp"
        ) as request:
            data = await request.json()
        level = data["level"]
        usernamelvl = username + level
        embed = discord.Embed(title=usernamelvl, color=0x8C05D2)
        if data["kills"] != "N/A":
            embed.add_field(name="Kills", value=data["kills"], inline=True)
        if data["kdRatio"] != "N/A":
            embed.add_field(name="K/D Ratio", value=data["kdRatio"], inline=True)
        if data["recordKillStreak"] != "N/A":
            embed.add_field(name="Highest Killstreak", value=data["recordKillStreak"], inline=True)
        if data["accuracy"] != "N/A":
            embed.add_field(name="Average Accuracy", value=data["accuracy"], inline=True)
        if data["wins"] != "N/A":
            embed.add_field(name="Total Wins", value=data["wins"], inline=True)
        if data["winLossRatio"] != "N/A":
            embed.add_field(name="Win/Loss Ratio", value=data["winLossRatio"], inline=True)
        if data["currentWinStreak"] != "N/A":
            embed.add_field(name="Current Win Streak", value=data["currentWinStreak"], inline=True)
        if data["gamesPlayed"] != "N/A":
            embed.add_field(name="Games Played", value=data["gamesPlayed"], inline=True)
        if data["scorePerMinute"] != "N/A":
            embed.add_field(name="Score Per Minute", value=data["scorePerMinute"], inline=True)
        if data["timePlayedTotal"] != "N/A":
            embed.add_field(name="Total Play Time (in minutes)", value=data["timePlayedTotal"], inline=True)
        embeds.append(embed)
        await menu(
            ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=20
        )
