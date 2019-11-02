import os
import discord

from redbot.core import Config, checks, commands
from redbot.core.data_manager import cog_data_path
from .announcer import Announcer
from .yaml_parse import embed_from_userstr


class ChangeLog(commands.Cog):
    """ChangeLogs"""

    __version__ = "1.0.1"

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=3468763865834, force_registration=True)
        default_guild = {"announce_ignore": True, "announce_channel": None}

        self.__current_announcer = None

        self.config.register_guild(**default_guild)

    def cog_unload(self):
        try:
            self.__current_announcer.cancel()
        except AttributeError:
            pass

    @staticmethod
    async def complain(ctx: commands.Context, message: str, **kwargs):
        await ctx.send(message.format(**kwargs))

    def is_announcing(self) -> bool:
        """
        Is the bot currently sending changelogs?
        :return:
        """
        if self.__current_announcer is None:
            return False

        return self.__current_announcer.active or False

    @commands.group(name="log", autohelp=True)
    async def _log(self, ctx: commands.Context):
        """
        Changelog commands
        """

    @_log.command(name="upload")
    @commands.bot_has_permissions(embed_links=True)
    @checks.is_owner()
    async def upload(self, ctx):
        """
        Upload new changelogs. \n
        An example changelog can be found in the changelog repo
        called changelog.yml.
        """
        try:
            direct = cog_data_path(self) / "changelog0.yml"
            change = cog_data_path(self) / "changelog1.yml"
            change1 = cog_data_path(self) / "changelog2.yml"
            if os.path.exists(change):
                os.rename(change, change1)
            if os.path.exists(direct):
                os.rename(direct, change)
            await ctx.message.attachments[0].save(direct)
            await ctx.send("Changelog updated")
            await self._autolog_send(ctx)
        except discord.HTTPException:
            await ctx.send("That didn't work.", delete_after=30)

    @_log.command(name="get", pass_context=True)
    @commands.bot_has_permissions(embed_links=True)
    async def get(self, ctx, number: str = 0):
        """
        Get changelogs for the bot
        """
        try:
            direct = cog_data_path(self) / "changelog{}.yml".format(number)
            await ctx.message.delete()
            info = open(direct, "r")
            data = info.read()
            embed = await embed_from_userstr(ctx, data)
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send("That changelog doesn't exist.", delete_after=30)

    @commands.group(name="autolog", autohelp=True)
    async def _autolog(self, ctx: commands.Context):
        """
        Autolog commands
        """

    async def _autolog_send(self, ctx: commands.Context):
        """Send out automatic changelogs"""

        direct = cog_data_path(self) / "changelog0.yml"
        await ctx.message.delete()
        info = open(direct, "r")
        data = info.read()
        message = await embed_from_userstr(ctx, data)
        if not self.is_announcing():
            announcer = Announcer(ctx, message, config=self.config)
            announcer.start()

            self.__current_announcer = announcer

            await ctx.send("The changelogs have started to send.")
        else:
            announcement = (
                "I am already sending changelogs. If you would like to cancel"
                " please use `{prefix}autolog cancel`"
                " first."
            )
            prefix = ctx.prefix
            await self.complain(ctx, announcement, prefix=prefix)
            await ctx.send("Changelogs sent.")

    @_autolog.command(name="cancel")
    @checks.is_owner()
    async def autolog_cancel(self, ctx):
        """Cancel a running changelog announcement."""
        try:
            self.__current_announcer.cancel()
        except AttributeError:
            pass

        await ctx.send("The current changelog has been canceled.")

    @_autolog.command(name="channel")
    @commands.guild_only()
    @checks.guildowner_or_permissions(administrator=True)
    async def autolog_channel(self, ctx, *, channel: discord.TextChannel = None):
        """Change the channel to which the bot sends automatic changelogs."""
        if channel is None:
            channel = ctx.channel
        await self.config.guild(ctx.guild).announce_channel.set(channel.id)

        await ctx.send(
            ("The changelog channel has been set to {channel.mention}").format(channel=channel)
        )

    @_autolog.command(name="ignore")
    @commands.guild_only()
    @checks.guildowner_or_permissions(administrator=True)
    async def autolog_ignore(self, ctx):
        """Toggle automatic changelogs being enabled this server."""
        ignored = await self.config.guild(ctx.guild).announce_ignore()
        await self.config.guild(ctx.guild).announce_ignore.set(not ignored)

        if ignored:
            await ctx.send(
                ("The server {guild.name} will receive automatic changelogs .").format(
                    guild=ctx.guild
                )
            )
        else:
            await ctx.send(
                ("The server {guild.name} will not receive automatic changelogs.").format(
                    guild=ctx.guild
                )
            )
