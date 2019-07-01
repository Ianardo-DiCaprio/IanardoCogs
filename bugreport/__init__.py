from .bugreport import BugReport


def setup(bot):
    bot.add_cog(BugReport(bot))
