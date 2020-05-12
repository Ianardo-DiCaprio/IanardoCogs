from .pdvote import PDvote


async def setup(bot):
    cog = PDvote(bot)
    bot.add_cog(cog)