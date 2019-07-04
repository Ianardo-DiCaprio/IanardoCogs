from .rand import Rand


def setup(bot):
    bot.add_cog(Rand(bot))
