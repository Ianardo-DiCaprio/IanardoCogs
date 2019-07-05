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
        """Command to set the IMDB API key
        You can aqquire an API key from
        http://www.omdbapi.com/apikey.aspx"""
        await self.conf.api_key.set(api_key)
        await ctx.send("The API key has been set.")
		
		
    @commands.command()
    async def imdbmovie(self, ctx, *, search):
        """Command to get information from IMDB"""
        api_key = await self.conf.api_key()
        search = search.replace(" ", "+")
        r = requests.get(("http://www.omdbapi.com/?apikey={api_key}&t={search}").format(api_key=api_key, search=search))
        data = r.json()
        try:
            title = data["Title"]
            poster = data["Poster"]
            run_time = data["Runtime"]
            release_date = data["Released"]
            imdb_rating = data["imdbRating"]
            age_rating = data["Rated"]
            plot = data["Plot"]
            genre = data["Genre"]
            director = data["Director"]
            actors = data["Actors"]
            box_office = data["BoxOffice"]
            embed=discord.Embed(title=title, color=0x8c05d2)
            embed.set_thumbnail(url=poster)
            embed.add_field(name="Run Time", value=run_time, inline=True)
            embed.add_field(name="Release Date", value=release_date, inline=True)
            embed.add_field(name="IMDB Rating", value=imdb_rating, inline=True)
            embed.add_field(name="Age Rating", value=age_rating, inline=True)
            embed.add_field(name="Plot", value=plot, inline=True)
            embed.add_field(name="Genre", value=genre, inline=True)
            embed.add_field(name="Director", value=director, inline=True)
            embed.add_field(name="Actors", value=actors, inline=True)
            embed.add_field(name="Box Office", value=box_office, inline=True)
            await ctx.send(embed=embed)
        except:
            await ctx.send("We couldn't find a movie with that name :worried:")

    @commands.command()
    async def imdbtv(self, ctx, *, search):
        """Command to get information from IMDB"""
        api_key = await self.conf.api_key()
        search = search.replace(" ", "+")
        r = requests.get(("http://www.omdbapi.com/?apikey={api_key}&t={search}").format(api_key=api_key, search=search))
        data = r.json()
        try:
            title = data["Title"]
            run_time = data["Runtime"] 
            poster = data["Poster"]
            release_date = data["Released"]
            imdb_rating = data["imdbRating"]
            age_rating = data["Rated"]
            plot = data["Plot"]
            genre = data["Genre"]
            director = data["Director"]
            actors = data["Actors"]
            seasons = data["totalSeasons"]
            embed=discord.Embed(title=title, color=0x8c05d2)
            embed.set_thumbnail(url=poster)
            embed.add_field(name="Average Run Time", value=run_time, inline=True)
            embed.add_field(name="Release Date", value=release_date, inline=True)
            embed.add_field(name="IMDB Rating", value=imdb_rating, inline=True)
            embed.add_field(name="Age Rating", value=age_rating, inline=True)
            embed.add_field(name="Plot", value=plot, inline=True)
            embed.add_field(name="Genre", value=genre, inline=True)
            embed.add_field(name="Director", value=director, inline=True)
            embed.add_field(name="Actors", value=actors, inline=True)
            embed.add_field(name="Seasons", value=seasons, inline=True)
            await ctx.send(embed=embed)
        except:
            await ctx.send("We couldn't find a TV show with that name :worried:")
(data.length > 75) ? data.substring[0,75] + '..' : data;

    @commands.command()
    async def socialb(self, ctx, *, search):
        """Command to get information from IMDB"""
        r = requests.get(("https://socialblade.com/youtube/user/{search}").format(search=search))
        please = (r.length > 600) ? data.substring[0,600] + '...' : r;
        await ctx.send(please)
