from .middleman import MiddleMan


def setup(bot):
    bot.add_cog(MiddleMan(bot))
