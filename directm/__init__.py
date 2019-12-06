from .directm import DirectM


async def setup(bot):
    cog = DirectM(bot)
    bot.add_cog(cog)
