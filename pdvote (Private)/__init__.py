from .pdvote import PDVote


async def setup(bot):
    cog = PDVote(bot)
    bot.add_cog(cog)
