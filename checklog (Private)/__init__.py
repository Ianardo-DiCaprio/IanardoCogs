from .checklog import CheckLog


async def setup(bot):
    cog = CheckLog(bot)
    bot.add_cog(cog)
