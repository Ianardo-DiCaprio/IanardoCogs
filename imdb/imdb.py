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
    async def imdb(self, ctx, *, search):
        """Command to get information from IMDB"""
        api_key = await self.conf.api_key()
        search = search.replace(" ", "+")
        r = requests.get(("http://www.omdbapi.com/?apikey={api_key}&t={search}").format(api_key=api_key, search=search))
        if website = "N/A"
            website = "https://cdn0.iconfinder.com/data/icons/interface-set-vol-2/50/No_data_No_info_Missing-512.png"
        else: 
            website = data["Website"] 
        data = r.json()
        title = data["Title"]
        website = data["Website"]
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
        embed=discord.Embed(title=title, url=website, color=0x8c05d2)
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
