import discord
from redbot.core import commands, checks, Config

class GamerTag(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, identifier=699114201327)
		
        default_member = {"gamertag": None}
		
        self.config.register_member(**default_member)
		
		
    @commands.command()
    async def gtset(self, ctx, gamertag = None):
        """Command to set yout gamertag"""
        user = ctx.user
        if gamertag:
            await self.config.user(user).gamertag.set(gamertag)
		    await ctx.send("Your gamertag has been set.")
        else:
            await self.config.gamertag.set(gamertag)
		    await ctx.send("Your gamertag has been removed.") 
		
		
    @commands.command()
    async def gt(self, ctx, user: discord.Member = None, gamertag):
        """Command to get a users gamertag if no user is given it will get yours."""
        try:
            if user is None:
                user = ctx.author
            gamertag = await self.config.user(user).gamertag()
            if gamertag:
                await ctx.send(f"This users gamertag is: {gamertag}")
        except:
            await ctx.send("This user hasn't set their gamertag.")
            
		
