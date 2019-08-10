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

    @commands.command()
    async def epicset(self, ctx, gamertag=None):
        """Command to set your Epic Games gamertag"""
        if gamertag:
            await self.conf.user(ctx.author).epicgamesgamertag.set(gamertag)
            await ctx.send("Your Epic Games gamertag has been set.")
        else:
            await self.conf.user(ctx.author).epicgamesgamertag.set(gamertag)
            await ctx.send("Your Epic Games gamertag has been removed.")

    @commands.command()
    async def bnicset(self, ctx, gamertag=None):
        """Command to set your Battle.net gamertag"""
        if gamertag:
            await self.conf.user(ctx.author).battlenetgamertag.set(gamertag)
            await ctx.send("Your Battle.net gamertag has been set.")
        else:
            await self.conf.user(ctx.author).battlenetgamertag.set(gamertag)
            await ctx.send("Your Battle.net gamertag has been removed.")

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

    @commands.command(aliases=["eggt"])
    async def eggamertag(self, ctx, user: discord.Member = None):
        """Command to get a users Epic Games gamertag if no user is given it will get yours."""
        if user is None:
            user = ctx.author
        eggamertag = await self.conf.user(user).epicgamesgamertag()
        if eggamertag:
            await ctx.send(f"This user's Epic Games gamertag is: {eggamertag}")
        else:
            await ctx.send("This user hasn't set an Epic Games gamertag.")

    @commands.command(aliases=["bngt"])
    async def bngamertag(self, ctx, user: discord.Member = None):
        """Command to get a users Battle.net gamertag if no user is given it will get yours."""
        if user is None:
            user = ctx.author
        bngamertag = await self.conf.user(user).battlenetgamertag()
        if bngamertag:
            await ctx.send(f"This user's Battle.net gamertag is: {bngamertag}")
        else:
            await ctx.send("This user hasn't set a Battle.net gamertag.")

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

    @commands.command()
    async def eglist(self, ctx):
        """Command to get a list of users Epic Games gamertags"""
        embeds = []
        msg = ""
        users = await self.conf.all_users()
        for user_id, gamertag in users.items():
            gamertagitems = gamertag.items()
            for k, v in gamertagitems:
                if "epicgamesgamertag" in k:
                        msg += f"<@{user_id}>'s Epic Games gamertag is: {v}\n"
        embed = discord.Embed(title="Epic Games gamertags", description=msg, color=0x8C05D2)
        embeds.append(embed)
        await menu(ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=20)

    @commands.command()
    async def bnlist(self, ctx):
        """Command to get a list of users Battle.net gamertags"""
        embeds = []
        msg = ""
        users = await self.conf.all_users()
        for user_id, gamertag in users.items():
            gamertagitems = gamertag.items()
            for k, v in gamertagitems:
                if "battlenetgamertag" in k:
                        msg += f"<@{user_id}>'s Battle.net gamertag is: {v}\n"
        embed = discord.Embed(title="Battle.net gamertags", description=msg, color=0x8C05D2)
        embeds.append(embed)
        await menu(ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=20)
