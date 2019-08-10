import discord
from redbot.core import commands, Config
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS


class GamerTag(commands.Cog):
    """GamerTag cog"""

    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, identifier=699114201327)

        default_user = {"gamertag": None}

        self.conf.register_user(**default_user)

    @commands.command()
    async def gtset(self, ctx, gamertag=None):
        """Command to set yout gamertag"""
        if gamertag:
            await self.conf.user(ctx.author).gamertag.set(gamertag)
            await ctx.send("Your gamertag has been set.")
        else:
            await self.conf.user(ctx.author).gamertag.set(gamertag)
            await ctx.send("Your gamertag has been removed.")

    @commands.command(aliases=["gt"])
    async def gamertag(self, ctx, user: discord.Member = None):
        """Command to get a users gamertag if no user is given it will get yours."""
        if user is None:
            user = ctx.author
        gamertag = await self.conf.user(user).gamertag()
        if gamertag:
            await ctx.send(f"This user's gamertag is: {gamertag}")
        else:
            await ctx.send("This user hasn't set a gamertag.")

    @commands.command()
    async def gtlist(self, ctx):
        """Command to get a users gamertag if no user is given it will get yours."""
        embeds = []
        msg = ""
        users = await self.conf.all_users()
        for user_id, gamertag in users.items():
            gamertagitems = gamertag.items()
            for gamer, tag in gamertagitems:
                msg += f"<@{user_id}>'s gamertag is: {tag}\n"
        embed = discord.Embed(title="Gamertags", description=msg, color=0x8C05D2)
        embeds.append(embed)
        await menu(ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=20)
