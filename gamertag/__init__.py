from .gamertag import GamerTag


async def setup(bot):
    cog = GamerTag(bot)
    bot.add_cog(cog)
