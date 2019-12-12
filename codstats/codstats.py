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
        username = username.replace(" ", "%20")
        username = username.replace("#", "%23")
        platform = platform.replace("pc", "battle")
        platform = platform.replace("xbox", "xbl")
        async with self._session.get(
                f"https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/{platform}/gamer/{username}/profile/type/mp"
            ) as request:
                data = await request.json()
        
        try:
            username = data["data"]["username"]
            level = round(data["data"]["level"])
            userlvl = f"{username} - Level: {level}"
            #Career Stats
            embed = discord.Embed(title=userlvl + " - Career Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            if data["data"]["lifetime"]["all"]["properties"]["totalShots"] != "N/A":
                embed.add_field(name="Total Shots", value=data["data"]["lifetime"]["all"]["properties"]["totalShots"], inline=True)
            if data["data"]["prestige"] != "N/A":
                embed.add_field(name="Prestige", value=data["data"]["prestige"], inline=True)
            if data["data"]["totalXp"] != "N/A":
                embed.add_field(name="Total XP", value=data["data"]["totalXp"], inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["timePlayedTotal"] != "N/A":
                embed.add_field(name="Total Playtime", value=data["data"]["lifetime"]["all"]["properties"]["timePlayedTotal"], inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["hits"] != "N/A":
                embed.add_field(name="Total Hits", value=data["data"]["lifetime"]["all"]["properties"]["hits"], inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["score"] != "N/A":
                embed.add_field(name="Total Score", value=data["data"]["lifetime"]["all"]["properties"]["score"], inline=True)
            embeds.append(embed)
            #Game Stats
            embed = discord.Embed(title=userlvl + " - Game Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            if data["data"]["lifetime"]["all"]["properties"]["wins"] != "N/A":
                embed.add_field(name="Total Wins", value=data["data"]["lifetime"]["all"]["properties"]["wins"], inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["losses"] != "N/A":
                embed.add_field(name="Total Losses", value=data["data"]["lifetime"]["all"]["properties"]["losses"], inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["winLossRatio"] != "N/A":
                embed.add_field(name="Win/Loss Ratio", value=data["data"]["lifetime"]["all"]["properties"]["winLossRatio"], inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["gamesPlayed"] != "N/A":
                embed.add_field(name="Total Games Played", value=data["data"]["lifetime"]["all"]["properties"]["gamesPlayed"], inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["kills"] != "N/A":
                embed.add_field(name="Total Kills", value=data["data"]["lifetime"]["all"]["properties"]["kills"], inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["deaths"] != "N/A":
                embed.add_field(name="Total Deaths", value=data["data"]["lifetime"]["all"]["properties"]["deaths"], inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["kdRatio"] != "N/A":
                embed.add_field(name="kill/Death Ratio", value=data["data"]["lifetime"]["all"]["properties"]["kdRatio"], inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["assists"] != "N/A":
                embed.add_field(name="Total Assists", value=data["data"]["lifetime"]["all"]["properties"]["assists"], inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["headshots"] != "N/A":
                embed.add_field(name="Total Headshots", value=data["data"]["lifetime"]["all"]["properties"]["headshots"], inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["scorePerGame"] != "N/A":
                embed.add_field(name="Score Per Game", value=data["data"]["lifetime"]["all"]["properties"]["scorePerGame"], inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["bestKills"] != "N/A":
                embed.add_field(name="Highest Kills In Game", value=data["data"]["lifetime"]["all"]["properties"]["bestKills"], inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["currentWinStreak"] != "N/A":
                embed.add_field(name="Current Win Streak", value=data["data"]["lifetime"]["all"]["properties"]["currentWinStreak"], inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["recordLongestWinStreak"] != "N/A":
                embed.add_field(name="Highest Ever Win Streak", value=data["data"]["lifetime"]["all"]["properties"]["recordLongestWinStreak"], inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["recordXpInAMatch"] != "N/A":
                embed.add_field(name="Highest Ever Score In Game", value=data["data"]["lifetime"]["all"]["properties"]["recordXpInAMatch"], inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["recordKillStreak"] != "N/A":
                embed.add_field(name="Highest Ever None Killsteak, Killstreak", value=data["data"]["lifetime"]["all"]["properties"]["recordKillStreak"], inline=True)
            embeds.append(embed)
            #killstreak Stats
            embed = discord.Embed(title=userlvl + " - Killstreak Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["precision_airstrike"]["properties"]["uses"] != "N/A":
                embed.add_field(name="Precision Airstrike", value=data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["precision_airstrike"]["properties"]["uses"], inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["cruise_predator"]["properties"]["uses"] != "N/A":
                embed.add_field(name="Cruise Predator", value=data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["cruise_predator"]["properties"]["uses"], inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["manual_turret"]["properties"]["uses"] != "N/A":
                embed.add_field(name="Manual Turret", value=data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["manual_turret"]["properties"]["uses"], inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["white_phosphorus"]["properties"]["uses"] != "N/A":
                embed.add_field(name="White Phosphorus", value=data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["white_phosphorus"]["properties"]["uses"], inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["hover_jet"]["properties"]["uses"] != "N/A":
                embed.add_field(name="Hover Jet", value=data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["hover_jet"]["properties"]["uses"], inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["chopper_gunner"]["properties"]["uses"] != "N/A":
                embed.add_field(name="Chopper Gunner", value=data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["chopper_gunner"]["properties"]["uses"], inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["gunship"]["properties"]["uses"] != "N/A":
                embed.add_field(name="Gunship", value=data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["gunship"]["properties"]["uses"], inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["sentry_gun"]["properties"]["uses"] != "N/A":
                embed.add_field(name="Sentry Gun", value=data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["sentry_gun"]["properties"]["uses"], inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["toma_strike"]["properties"]["uses"] != "N/A":
                embed.add_field(name="Toma Strike", value=data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["toma_strike"]["properties"]["uses"], inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["nuke"]["properties"]["uses"] != "N/A":
                embed.add_field(name="Nuke", value=data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["nuke"]["properties"]["uses"], inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["juggernaut"]["properties"]["uses"] != "N/A":
                embed.add_field(name="Juggernaut", value=data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["juggernaut"]["properties"]["uses"], inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["pac_sentry"]["properties"]["uses"] != "N/A":
                embed.add_field(name="Pac Sentry", value=data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["pac_sentry"]["properties"]["uses"], inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["chopper_support"]["properties"]["uses"] != "N/A":
                embed.add_field(name="Chopper Support", value=data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["chopper_support"]["properties"]["uses"], inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["bradley"]["properties"]["uses"] != "N/A":
                embed.add_field(name="Bradley", value=data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["bradley"]["properties"]["uses"], inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["airdrop"]["properties"]["uses"] != "N/A":
                embed.add_field(name="Air Drop", value=data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["airdrop"]["properties"]["uses"], inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["radar_drone_overwatch"]["properties"]["uses"] != "N/A":
                embed.add_field(name="Radar Drone Overwatch", value=data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["radar_drone_overwatch"]["properties"]["uses"], inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["scrambler_drone_guard"]["properties"]["uses"] != "N/A":
                embed.add_field(name="Scrambler Drone Guard", value=data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["scrambler_drone_guard"]["properties"]["uses"], inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["uav"]["properties"]["uses"] != "N/A":
                embed.add_field(name="UAV", value=data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["uav"]["properties"]["uses"], inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["airdrop_multiple"]["properties"]["uses"] != "N/A":
                embed.add_field(name="Airdrop Multiple", value=data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["airdrop_multiple"]["properties"]["uses"], inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["directional_uav"]["properties"]["uses"] != "N/A":
                embed.add_field(name="Directional UAV", value=data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["directional_uav"]["properties"]["uses"], inline=True)
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=60
            )
        except:
            await ctx.send("Either the platform or username is incorrect, please make sure to use pc, psn or xbox for the platform and make sure you spelt your name correctly.")
