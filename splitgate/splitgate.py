import discord
import aiohttp
from redbot.core import commands, checks, Config
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from redbot.core.utils.chat_formatting import pagify
from typing import Optional

class SPLITGATE(commands.Cog):
    """"Simple Commands to get stats for Splitgate"""

    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, identifier=699113442013)

        self._session = aiohttp.ClientSession()

        default_user = {
            "platform": None,
            "username": None,
        }

        self.conf.register_user(**default_user)

    def cog_unload(self):
        self.bot.loop.create_task(self._session.close())

    @commands.command()
    async def splitgatepset(self, ctx, platform=None):
        """Command to set Splitgate platform"""
        if platform:
            await self.conf.user(ctx.author).platform.set(platform)
            await ctx.send("Your platform has been set.")
        else:
            await self.conf.user(ctx.author).platform.set(platform)
            await ctx.send("Your platform has been removed.")

    @commands.command()
    async def splitgateuset(self, ctx, username=None):
        """Command to set Splitgate username"""
        if username:
            await self.conf.user(ctx.author).username.set(username)
            await ctx.send("Your username has been set.")
        else:
            await self.conf.user(ctx.author).username.set(username)
            await ctx.send("Your username has been removed.")
    @commands.command()
    async def splitgatestats(self, ctx, platform: Optional[str] = "", *, username: Optional[str] = ""):
        """Command to get your Splitgate stats
        For platform use pc, xbox, psn"""
        embeds = []
        if platform + username == "":
            user = ctx.author
            platform = await self.conf.user(user).platform()
            username = await self.conf.user(user).username()
        username = username.replace(" ", "%20")
        platform = platform.replace("xbox", "xbl")
        headers = {'TRN-Api-Key':'91b58a5a-5df3-4292-82f3-6262c829709d'}
        async with self._session.get(
                f"https://public-api.tracker.gg/v2/splitgate/standard/profile/{platform}/{username}",headers=headers
            ) as request:
                data = await request.json()
        username = data["data"]["platformInfo"]["platformUserHandle"]
        embed = discord.Embed(title="Splitgate Stats", color=0x8C05D2)
        if data["data"]["platformInfo"]["platformUserHandle"] != "N/A":
            username = data["data"]["platformInfo"]["platformUserHandle"]
            embed.add_field(name="**Username:**", value=username, inline=True)
        if data["data"]["segments"][0]["stats"]["kills"]["value"] != "N/A":
            kills = data["data"]["segments"][0]["stats"]["kills"]["value"]
            embed.add_field(name="**kills:**", value=kills, inline=True)
        embeds.append(embed)
        await menu(
            ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=180)
        
