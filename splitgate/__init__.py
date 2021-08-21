from .splitgate import SPLITGATE


async def setup(bot):
    cog = SPLITGATE(bot)
    bot.add_cog(cog)