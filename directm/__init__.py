from .directm import DirectM


async def setup(bot):
    DirectM = DirectM(bot)
    bot.add_cog(DirectM)