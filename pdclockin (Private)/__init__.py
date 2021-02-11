from .pdclockin import PDClockin


async def setup(bot):
    cog = PDClockin(bot)
    bot.add_cog(cog)
