import discord
import aiohttp
from redbot.core import commands, checks, Config
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from redbot.core.utils.chat_formatting import pagify
from typing import Optional

class CODSTATS(commands.Cog):
    """"Simple Commands to get stats for COD"""

    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, identifier=6991142013)

        self._session = aiohttp.ClientSession()

        default_user = {
            "platform": None,
            "username": None,
        }

        self.conf.register_user(**default_user)

    def cog_unload(self):
        self.bot.loop.create_task(self._session.close())

    @commands.command()
    async def codpset(self, ctx, platform=None):
        """Command to set COD platform"""
        if platform:
            await self.conf.user(ctx.author).platform.set(platform)
            await ctx.send("Your platform has been set.")
        else:
            await self.conf.user(ctx.author).platform.set(platform)
            await ctx.send("Your platform has been removed.")

    @commands.command()
    async def coduset(self, ctx, username=None):
        """Command to set COD username"""
        if username:
            await self.conf.user(ctx.author).username.set(username)
            await ctx.send("Your username has been set.")
        else:
            await self.conf.user(ctx.author).username.set(username)
            await ctx.send("Your username has been removed.")

    @commands.command()
    async def codstats(self, ctx, platform: Optional[str] = "", *, username: Optional[str] = ""):
        """Command to get your COD: MW stats
        For platform use pc, xbox, psn"""
        embeds = []
        if platform + username == "":
            user = ctx.author
            platform = await self.conf.user(user).platform()
            username = await self.conf.user(user).username()
        platform = platform.replace("pc", "battle")
        platform = platform.replace("xbox", "xbl")
        username = username.replace(" ", "%20")
        username = username.replace("#", "%23")
        try:
            if platform == "pc" or "xbl" or "psn":
                async with self._session.get(
                        f"https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/{platform}/gamer/{username}/profile/type/mp"
                ) as request:
                    data = await request.json()
        except:
            await ctx.send("That platform doesn't exist, please use pc, xbox or psn.")
            return
        
        try:
            username = data["data"]["username"]
            level = round(data["data"]["level"])
            userlvl = f"{username} - Level: {level}"
            embed = discord.Embed(title=userlvl, color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            if data["data"]["lifetime"]["all"]["properties"]["kills"] != "N/A":
                kills = round(data["data"]["lifetime"]["all"]["properties"]["kills"])
                embed.add_field(name="Kills", value=kills, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["kdRatio"] != "N/A":
                killd = round(data["data"]["lifetime"]["all"]["properties"]["kdRatio"], 2)
                embed.add_field(name="K/D Ratio", value=killd, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["recordKillStreak"] != "N/A":
                recordKillStreak = round(data["data"]["lifetime"]["all"]["properties"]["recordKillStreak"])
                embed.add_field(name="Highest Killstreak", value=recordKillStreak, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["accuracy"] != "N/A":
                accuracy = round(data["data"]["lifetime"]["all"]["properties"]["accuracy"], 2)
                embed.add_field(name="Average Accuracy", value=accuracy, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["wins"] != "N/A":
                wins = round(data["data"]["lifetime"]["all"]["properties"]["wins"])
                embed.add_field(name="Total Wins", value=wins, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["winLossRatio"] != "N/A":
                winloss = round(data["data"]["lifetime"]["all"]["properties"]["winLossRatio"], 2)
                embed.add_field(name="Win/Loss Ratio", value=winloss, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["currentWinStreak"] != "N/A":
                currentWinStreak = round(data["data"]["lifetime"]["all"]["properties"]["currentWinStreak"])
                embed.add_field(name="Current Win Streak", value=currentWinStreak, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["gamesPlayed"] != "N/A":
                gamesPlayed = round(data["data"]["lifetime"]["all"]["properties"]["gamesPlayed"])
                embed.add_field(name="Games Played", value=gamesPlayed, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["scorePerMinute"] != "N/A":
                scorepm = round(data["data"]["lifetime"]["all"]["properties"]["scorePerMinute"], 2)
                embed.add_field(name="Score Per Minute", value=scorepm, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["timePlayedTotal"] != "N/A":
                timePlayedTotal = round(data["data"]["lifetime"]["all"]["properties"]["timePlayedTotal"])
                embed.add_field(name="Total Play Time (in minutes)", value=timePlayedTotal, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["nuke"]["properties"]["uses"] != "N/A":
                nuke = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["nuke"]["properties"]["uses"])
                embed.add_field(name="Nukes", value=nuke, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["juggernaut"]["properties"]["uses"] != "N/A":
                juggernaut = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["juggernaut"]["properties"]["uses"])
                embed.add_field(name="Juggernaut", value=juggernaut, inline=True)
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=20
            )
        except:
            await ctx.send("We couldn't find that profile on that platform")
