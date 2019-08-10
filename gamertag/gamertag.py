import discord
from redbot.core import commands, Config
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS


class GamerTag(commands.Cog):
    """GamerTag cog"""

    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, identifier=699114201327)

        default_user = {
            "playlstationgamertag": None,
            "xboxgamertag": None,
            "epicgamesgamertag": None,
            "battlenetgamertag": None,
            "uplaygamertag": None,
            "steamgamertag": None,
            }

        self.conf.register_user(**default_user)

    @commands.command()
    async def psset(self, ctx, gamertag=None):
        """Command to set your playstation gamertag"""
        if gamertag:
            await self.conf.user(ctx.author).playstationgamertag.set(gamertag)
            await ctx.send("Your playstation gamertag has been set.")
        else:
            await self.conf.user(ctx.author).playsationgamertag.set(gamertag)
            await ctx.send("Your playstation gamertag has been removed.")

    @commands.command()
    async def xbset(self, ctx, gamertag=None):
        """Command to set your Xbox gamertag"""
        if gamertag:
            await self.conf.user(ctx.author).xboxgamertag.set(gamertag)
            await ctx.send("Your Xbox gamertag has been set.")
        else:
            await self.conf.user(ctx.author).xboxgamertag.set(gamertag)
            await ctx.send("Your Xbox gamertag has been removed.")

    @commands.command(aliases=["psgt"])
    async def psgamertag(self, ctx, user: discord.Member = None):
        """Command to get a users Playstation gamertag if no user is given it will get yours."""
        if user is None:
            user = ctx.author
        psgamertag = await self.conf.user(user).playstationgamertag()
        if psgamertag:
            await ctx.send(f"This user's Playstation gamertag is: {psgamertag}")
        else:
            await ctx.send("This user hasn't set a Playstation gamertag.")

    @commands.command(aliases=["xbgt"])
    async def xbgamertag(self, ctx, user: discord.Member = None):
        """Command to get a users Xbox gamertag if no user is given it will get yours."""
        if user is None:
            user = ctx.author
        xbgamertag = await self.conf.user(user).xboxgamertag()
        if xbgamertag:
            await ctx.send(f"This user's Xbox gamertag is: {xbgamertag}")
        else:
            await ctx.send("This user hasn't set a Xbox gamertag.")

    @commands.command()
    async def pslist(self, ctx):
        """Command to get a list of users Playstation gamertags"""
        embeds = []
        msg = ""
        users = await self.conf.all_users()
        for user_id, gamertag in users.items():
            gamertagitems = gamertag.items()
            for k, v in gamertagitems:
                if "playstationgamertag" in k:
                        msg += f"<@{user_id}>'s Playstation gamertag is: {v}\n"
        embed = discord.Embed(title="Playstation gamertags", description=msg, color=0x8C05D2)
        embeds.append(embed)
        await menu(ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=20)

    @commands.command()
    async def xblist(self, ctx):
        """Command to get a list of users Xbox gamertags"""
        embeds = []
        msg = ""
        users = await self.conf.all_users()
        for user_id, gamertag in users.items():
            gamertagitems = gamertag.items()
            for k, v in gamertagitems:
                if "xboxgamertag" in k:
                        msg += f"<@{user_id}>'s Xbox gamertag is: {v}\n"
        embed = discord.Embed(title="Xbox gamertags", description=msg, color=0x8C05D2)
        embeds.append(embed)
        await menu(ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=20)
