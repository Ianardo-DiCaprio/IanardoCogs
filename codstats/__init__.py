from .codstats import CODSTATS


async def setup(bot):
    cog = CODSTATS(bot)
    bot.add_cog(cog)