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

    @commands.command(aliases=["psgt"])
    async def psgamertag(self, ctx, user: discord.Member = None):
        """Command to get a users Playstation gamertag if no user is given it will get yours."""
        if user is None:
            user = ctx.author
        psgamertag = await self.conf.user(user).playsationgamertag()
        if psgamertag:
            await ctx.send(f"This user's Playstation gamertag is: {psgamertag}")
        else:
            await ctx.send("This user hasn't set a Playstation gamertag.")

    @commands.command()
    async def psgtlist(self, ctx):
        """Command to get a list of users Playstation gamertags"""
        embeds = []
        msg = ""
        users = await self.conf.all_users()
        for user_id, playstationgamertag in users.items():
            gamertagitems = playstationgamertag.items()
            for gamer, tag in gamertagitems:
                msg += f"<@{user_id}>'s Playstation gamertag is: {tag}\n"
        embed = discord.Embed(title="Gamertags", description=msg, color=0x8C05D2)
        embeds.append(embed)
        await menu(ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=20)
