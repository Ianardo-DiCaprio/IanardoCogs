import discord
import aiohttp
from redbot.core import commands, checks, Config
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from redbot.core.utils.chat_formatting import pagify


class IMDB(commands.Cog):
    """"Simple Commands to get info from IMDB"""

    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, identifier=6991142013)

        self.conf.register_global(api_key=None)
        self._session = aiohttp.ClientSession()

    def cog_unload(self):
        self.bot.loop.create_task(self._session.close())

    @commands.command()
    @checks.is_owner()
    async def imdbapi(self, ctx, api_key):
        """Command to set the IMDB API key
        You can aqquire an API key from
        http://www.omdbapi.com/apikey.aspx"""
        await self.conf.api_key.set(api_key)
        await ctx.send("The API key has been set.")

    @commands.command()
    async def movie(self, ctx, *, search):
        """Command to get information for Movies
       from IMDB"""
        embeds = []
        api_key = await self.conf.api_key()
        search = search.replace(" ", "+")
        async with self._session.get(
                f"http://www.omdbapi.com/?apikey={api_key}&t={search}"
        ) as request:
            data = await request.json()
        try:
            title = data["Title"]
            embed = discord.Embed(title=title, color=0x8C05D2)
            if data["Poster"] != "N/A":
                embed.set_thumbnail(url=data["Poster"])
            if data["imdbID"]:
                embed.url = "http://www.imdb.com/title/{}".format(data["imdbID"])
            if data["Runtime"]:
                embed.add_field(name="Run Time", value=data["Runtime"], inline=True)
            if data["Released"]:
                embed.add_field(name="Release Date", value=data["Released"], inline=True)
            if data["imdbRating"]:
                embed.add_field(name="IMDB Rating", value=data["imdbRating"], inline=True)
            if data["Rated"]:
                embed.add_field(name="Age Rating", value=data["Rated"], inline=True)
            if data["Plot"]:
                embed.add_field(name="Plot", value=data["Plot"], inline=False)
            if data["Genre"]:
                embed.add_field(name="Genre", value=data["Genre"], inline=True)
            if data["Director"]:
                embed.add_field(name="Director", value=data["Director"], inline=True)
            if data["Actors"]:
                embed.add_field(name="Actors", value=data["Actors"], inline=True)
            if data["BoxOffice"]:
                embed.add_field(name="Box Office", value=data["BoxOffice"], inline=True)
            if data["Production"]:
                embed.add_field(name="Production", value=data["Production"], inline=True)
            if data["Language"]:
                embed.add_field(name="Language", value=data["Language"], inline=True)
            if data["Country"]:
                embed.add_field(name="Country", value=data["Country"], inline=True)
            if data["Writer"]:
                embed.add_field(name="Writers", value=data["Writer"], inline=False)
            if data["Awards"]:
                embed.add_field(name="Awards", value=data["Awards"], inline=False)
            if data["Website"]:
                embed.set_footer(text=data["Website"])
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=20
            )
        except KeyError:
            await ctx.send("We couldn't find a movie with that name :worried:")

    @commands.command()
    async def show(self, ctx, *, search):
        """Command to get information for
        TV shows from IMDB"""
        embeds = []
        api_key = await self.conf.api_key()
        search = search.replace(" ", "+")
        async with self._session.get(
                f"http://www.omdbapi.com/?apikey={api_key}&t={search}&plot=full"
        ) as request:
            data = await request.json()
        try:
            title = data["Title"]
            embed = discord.Embed(title=title, color=0x8C05D2)
            if data["Runtime"]:
                embed.add_field(name="Average Run Time", value=data["Runtime"], inline=True)
            if data["imdbID"]:
                embed.url = "http://www.imdb.com/title/{}".format(data["imdbID"])
            if data["Poster"]:
                embed.set_thumbnail(url=data["Poster"])
            if data["Released"]:
                embed.add_field(name="Release Date", value=data["Released"], inline=True)
            if data["imdbRating"]:
                embed.add_field(name="IMDB Rating", value=data["imdbRating"], inline=True)
            if data["Rated"]:
                embed.add_field(name="Age Rating", value=data["Rated"], inline=True)
            if data["Plot"]:
                embed.add_field(name="Plot", value=data["Plot"], inline=False)
            if data["Genre"]:
                embed.add_field(name="Genre", value=data["Genre"], inline=True)
            if data["Director"]:
                embed.add_field(name="Director", value=data["Director"], inline=True)
            if data["Actors"]:
                embed.add_field(name="Actors", value=data["Actors"], inline=True)
            if data["totalSeasons"]:
                embed.add_field(name="Seasons", value=data["totalSeasons"], inline=True)
            if data["Language"]:
                embed.add_field(name="Language", value=data["Language"], inline=True)
            if data["Country"]:
                embed.add_field(name="Country", value=data["Country"], inline=True)
            if data["Writer"]:
                embed.add_field(name="Writers", value=data["Writer"], inline=False)
            if data["Awards"]:
                embed.add_field(name="Awards", value=data["Awards"], inline=False)
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=20
            )
        except KeyError:
            await ctx.send("We couldn't find a TV show with that name :worried:")
