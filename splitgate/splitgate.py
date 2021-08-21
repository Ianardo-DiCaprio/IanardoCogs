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
        username = username.replace("#", "%23")
        platform = platform.replace("pc", "battle")
        platform = platform.replace("xbox", "xbl")
        async with self._session.get(
                f"https://public-api.tracker.gg/v2/splitgate/standard/profile/psn/Kill_Switch_YT7"
            ) as request:
                data = await request.json()
        try:
            username = data["platformInfo"]["platformUserHandle"]
            #Career Stats
            embed = discord.Embed(title="Username", color=0x8C05D2)
            if data["platformInfo"]["platformUserHandle"] != "N/A":
                username = data["platformInfo"]["platformUserHandle"]
                embed.add_field(name="**Username:**", value=username, inline=True)
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=180
            )
        except:
            await ctx.send("Either the platform or username is incorrect, please make sure to use pc, psn or xbox for the platform and make sure you spelt your name correctly. Or this is still broken")
        