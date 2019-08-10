import discord
from redbot.core import commands, checks, Config

class GamerTag(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, identifier=699114201327)
		
        default_user = {"gamertag": None}
		
        self.conf.register_user(**default_user)
		
		
    @commands.command()
    async def gtset(self, ctx, gamertag = None):
        """Command to set yout gamertag"""
        if gamertag:
            await self.conf.user(ctx.author).gamertag.set(gamertag)
            await ctx.send("Your gamertag has been set.")
        else:
            await self.conf.user(ctx.author).gamertag.set(gamertag)
            await ctx.send("Your gamertag has been removed.") 
		
		
    @commands.command()
    async def gt(self, ctx, user: discord.Member = None):
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
        users = await self.conf.all_users()
        for user_id, gamertag.keys in users.items():
            await ctx.send(f"<@{user_id}> gamertag is {gamertag}")
            
		
