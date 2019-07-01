from . import changelog


def setup(bot):
    bot.add_cog(changelog.ChangeLog(bot))
