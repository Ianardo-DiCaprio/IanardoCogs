import discord
import requests
import json
from redbot.core import commands, checks, Config
from redbot.core.utils.menus import menu, commands, DEFAULT_CONTROLS

class IMDB(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, identifier=6991142013)
		
        self.conf.register_global(api_key=None)

    @commands.command()
    @checks.is_owner()
    async def imdbapi(self, ctx, api_key):
        """Command to set the IMDB API key
        You can aqquire an API key from
        http://www.omdbapi.com/apikey.aspx"""
        await self.conf.api_key.set(api_key)
        await ctx.send("The API key has been set.")
		
		
    @commands.command()
    async def imdbmovie(self, ctx, *, search):
        """Command to get information for Movies 
       from IMDB"""
        embeds = []
        api_key = await self.conf.api_key()
        search = search.replace(" ", "+")
        r = requests.get(("http://www.omdbapi.com/?apikey={api_key}&t={search}").format(api_key=api_key, search=search))
        data = r.json()
        try:
            title = data["Title"]
            embed=discord.Embed(title=title, color=0x8c05d2)
            if data["Poster"]:
                embed.set_thumbnail(url=data['Poster'])
            if data["Runtime"]:
                embed.add_field(name="Run Time", value=data["Runtime"], inline=True)
            if data["Released"]:
                embed.add_field(name="Release Date", value=data["Released"], inline=True)
            if data["imdbRating"]:
                embed.add_field(name="IMDB Rating", value=data["imdbRating"], inline=True)
            if data["Rated"]:
                embed.add_field(name="Age Rating", value=data["Rated"], inline=True)
            if data["Plot"]:
                embed.add_field(name="Plot", value=data["Plot"], inline=True)
            if data["Genre"]:
                embed.add_field(name="Genre", value=data["Genre"], inline=True)
            if data["Director"]:
                embed.add_field(name="Director", value=data["Director"], inline=True)
            if data["Actors"]:
                embed.add_field(name="Actors", value=data["Actors"], inline=True)
            if data["BoxOffice"]:
                embed.add_field(name="Box Office", value=data["BoxOffice"], inline=True)
            embeds.append(embed)
            await menu(ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=20)
        except:
            await ctx.send("We couldn't find a movie with that name :worried:")

    @commands.command()
    async def imdbtv(self, ctx, *, search):
        """Command to get information for
        TV shows from IMDB"""
        embeds = []
        api_key = await self.conf.api_key()
        search = search.replace(" ", "+")
        r = requests.get(("http://www.omdbapi.com/?apikey={api_key}&t={search}").format(api_key=api_key, search=search))
        data = r.json()
        try:
            title = data["Title"]
            embed=discord.Embed(title=title, color=0x8c05d2)
            if data["Runtime"]:
                embed.add_field(name="Average Run Time", value=data["Runtime"], inline=True)
            if data['imdbID']:
                embed.url = "http://www.imdb.com/title/{}".format(data['imdbID'])
            if data["Poster"]:
                embed.set_thumbnail(url=data["Poster"])
            if data["Released"]:
                embed.add_field(name="Release Date", value=data["Released"], inline=True)
            if data["imdbRating"]:
                embed.add_field(name="IMDB Rating", value=data["imdbRating"], inline=True)
            if data["Rated"]:
                embed.add_field(name="Age Rating", value=data["Rated"], inline=True)
            if data["Plot"]:
                embed.add_field(name="Plot", value=data["Plot"], inline=True)
            if data["Genre"]:
                embed.add_field(name="Genre", value=data["Genre"], inline=True)
            if data["Director"]:
                embed.add_field(name="Director", value=data["Director"], inline=True)
            if data["Actors"]:
                embed.add_field(name="Actors", value=data["Actors"], inline=True)
            if data["totalSeasons"]:
                embed.add_field(name="Seasons", value=data["totalSeasons"], inline=True)
            embeds.append(embed)
            await menu(ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=20)
        except:
            await ctx.send("We couldn't find a movie with that name :worried:")

