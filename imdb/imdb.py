import discord
from redbot.core import commands, checks, Config

class IMDB(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, identifier=6991142013)
		
        self.conf.register_global(api_key=None)

    @commands.command()
    @checks.is_owner()
    async def imdbapi(self, ctx, api_key):
        """Command to set the IMDB API key"""
        await self.config.api_key.set(api_key)
        await ctx.send("The API key has been set.")
		
		
    @commands.command()
    async def imdb(self, ctx, search):
        """Command to get information from IMDB"""
        api_key = await self.conf.api_key()
        search = search.replace(" ", "+")
        response = unirest.get("https://movie-database-imdb-alternative.p.rapidapi.com/?page=1&r=json&s={search}",
        headers={
        "X-RapidAPI-Host": "movie-database-imdb-alternative.p.rapidapi.com",
        }
        ).format(search=search)
        await ctx.send(response)
		
