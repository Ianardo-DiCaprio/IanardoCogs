from .imdb import IMDB


async def setup(bot):
    cog = IMDB(bot)
    bot.add_cog(cog)
