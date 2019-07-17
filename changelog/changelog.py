import io
import contextlib
import os

import discord
from redbot.core import Config
from redbot.core import checks
from redbot.core import commands
from redbot.core.data_manager import cog_data_path
from .announcer import Announcer

from .utils import parse_time
from .yaml_parse import embed_from_userstr

class ChangeLog(commands.Cog):
    """
    ChangeLogs
    """

    __version__ = "1.0.0"


    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=3468763865834, force_registration=True
        )
        default_guild = {
            "announce_ignore": True,
            "announce_channel": None,
        }
        
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
        
    def check(m):
        return m.id == ctx.message.id or m.author == victim

    @commands.group(name="log", autohelp=True)
    async def _log(self, ctx: commands.Context):
        """
        Changelog commands
        """
        pass
        
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
            with io.BytesIO() as fp:
                dir = cog_data_path(self) / "changelog0.yml"
                a = cog_data_path(self) / "changelog1.yml"
                b = cog_data_path(self) / "changelog2.yml"
                if os.path.exists(a):
                    os.rename(a, b)
                if os.path.exists(dir):
                    os.rename(dir, a)
                await ctx.message.attachments[0].save(dir)
                await ctx.send("Changelog updated")
                await self._autolog_send(ctx)
        except Exception:
            await ctx.send("That didn't work.", delete_after=30)

    @_log.command(name="get", pass_context=True)
    @commands.bot_has_permissions(embed_links=True)
    async def get(self, ctx, number : str = 0):
        """
        Get changelogs for the bot
        """
        try:
            dir = cog_data_path(self) / "changelog{}.yml".format(number)
            await ctx.message.delete()
            fp = open(dir, "r")
            data = fp.read()
            e = await embed_from_userstr(ctx, data)
            await ctx.send(embed=e)
        except Exception:
            await ctx.send("That changelog doesn't exist.", delete_after=30)
    
    @commands.group(name="autolog", autohelp=True)
    async def _autolog(self, ctx: commands.Context):
        """
        Autolog commands
        """
        pass
        
    async def _autolog_send(self, ctx: commands.Context):
        """Send out automatic changelogs"""
        
        dir = cog_data_path(self) / "changelog0.yml"
        await ctx.message.delete()
        fp = open(dir, "r")
        data = fp.read()
        message = await embed_from_userstr(ctx, data)
        if not self.is_announcing():
            announcer = Announcer(ctx, message, config=self.config)
            announcer.start()

            self.__current_announcer = announcer

            await ctx.send("The changelogs have started to send.")
        else:
            RUNNING_ANNOUNCEMENT = (
            "I am already sending changelogs. If you would like to cancel"
            " please use `{prefix}autolog cancel`"
            " first.")
            prefix = ctx.prefix
            await self.complain(ctx, RUNNING_ANNOUNCEMENT, prefix=prefix)
            await ctx.send("Changelogs sent.")

    @_autolog.command(name="cancel")
    @checks.is_owner()
    async def autolog_cancel(self, ctx):
        """Cancel a running changelog anniouncement."""
        try:
            self.__current_announcer.cancel()
        except AttributeError:
            pass

        await ctx.send("The current changelog embed has been canceled.")

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
                ("The server {guild.name} will receive automatic changelogs .").format(guild=ctx.guild)
            )
        else:
            await ctx.send(
                ("The server {guild.name} will not receive automatic changelogs.").format(
                    guild=ctx.guild
                )
            )
