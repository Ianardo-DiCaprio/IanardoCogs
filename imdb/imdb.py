import discord
import requests
import json
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
        await self.conf.api_key.set(api_key)
        await ctx.send("The API key has been set.")
		
		
    @commands.command()
    async def imdb(self, ctx, search):
        """Command to get information from IMDB"""
        api_key = await self.conf.api_key()
        search = search.replace(" ", "+")
        r = requests.get(("http://www.omdbapi.com/?apikey={api_key}&s={search}").format(api_key=api_key, search=search))
        data = r.json()
        title = data["Title"]
        age_rating = data["Rated"]
        release_date = data["Released"]
        genre = data["Genre"]
        director = data["Director"]
        actors = data["Actors"]
        plot = data["Plot"]
        imdb_rating = data["imdbRating"]
        embed=discord.Embed(title=title)
        embed.set_thumbnail(url="https://m.media-amazon.com/images/M/MV5BMTAwMjU5OTgxNjZeQTJeQWpwZ15BbWU4MDUxNDYxODEx._V1_SX300.jpg")
        embed.add_field(name="Age rating", value=age_rating, inline=False)
        embed.add_field(name="Release Date", value=release_date, inline=False)
        embed.add_field(name="Genre", value=genre, inline=False)
        embed.add_field(name="Director", value=director, inline=False)
        embed.add_field(name="Actors", value=actors, inline=False)
        embed.add_field(name="Plot", value=plot, inline=False)
        embed.add_field(name="IMDB Rating", value=imdb_rating, inline=False)
        await ctx.send(embed=embed)
