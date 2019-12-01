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
        username = data["data"]["username"]
        level = data["data"]["level"]
        userlvl = f"{username} - Level: {level}"
        embed = discord.Embed(title=userlvl, color=0x8C05D2)
        if data["data"]["lifetime"]["all"]["properties"]["kills"] != "N/A":
            embed.add_field(name="Kills", value=data["data"]["lifetime"]["all"]["properties"]["kills"], inline=True)
        if data["data"]["lifetime"]["all"]["properties"]["kdRatio"] != "N/A":
            embed.add_field(name="K/D Ratio", value=data["data"]["lifetime"]["all"]["properties"]["kdRatio"], inline=True)
        if data["data"]["lifetime"]["all"]["properties"]["recordKillStreak"] != "N/A":
            embed.add_field(name="Highest Killstreak", value=data["data"]["lifetime"]["all"]["properties"]["recordKillStreak"], inline=True)
        if data["data"]["lifetime"]["all"]["properties"]["accuracy"] != "N/A":
            accuracy = int(data["data"]["lifetime"]["all"]["properties"]["accuracy"])
            accuracy1 = round(int(accuracy, 3))
            embed.add_field(name="Average Accuracy", value=accuracy1, inline=True)
        if data["data"]["lifetime"]["all"]["properties"]["wins"] != "N/A":
            embed.add_field(name="Total Wins", value=data["data"]["lifetime"]["all"]["properties"]["wins"], inline=True)
        if data["data"]["lifetime"]["all"]["properties"]["winLossRatio"] != "N/A":
            embed.add_field(name="Win/Loss Ratio", value=data["data"]["lifetime"]["all"]["properties"]["winLossRatio"], inline=True)
        if data["data"]["lifetime"]["all"]["properties"]["currentWinStreak"] != "N/A":
            embed.add_field(name="Current Win Streak", value=data["data"]["lifetime"]["all"]["properties"]["currentWinStreak"], inline=True)
        if data["data"]["lifetime"]["all"]["properties"]["gamesPlayed"] != "N/A":
            embed.add_field(name="Games Played", value=data["data"]["lifetime"]["all"]["properties"]["gamesPlayed"], inline=True)
        if data["data"]["lifetime"]["all"]["properties"]["scorePerMinute"] != "N/A":
            embed.add_field(name="Score Per Minute", value=data["data"]["lifetime"]["all"]["properties"]["scorePerMinute"], inline=True)
        if data["data"]["lifetime"]["all"]["properties"]["timePlayedTotal"] != "N/A":
            embed.add_field(name="Total Play Time (in minutes)", value=data["data"]["lifetime"]["all"]["properties"]["timePlayedTotal"], inline=True)
        embeds.append(embed)
        await menu(
            ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=20
        )
