from typing import Any
import datetime
import asyncio
import discord

from redbot.core import Config, checks, commands
from redbot.core.bot import Red
from redbot.core.utils.predicates import MessagePredicate, ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions
from datetime import datetime
from pytz import timezone

Cog: Any = getattr(commands, "Cog", object)


class PDClockin(Cog):
    """
    Simple LFG commands
    """

    __author__ = "Ianardo DiCaprio"
    __version__ = "1.0.0"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, 699114013, force_registration=True)

        default_user = {
            "name": None, 
            "message": None
        }
        default_guild = {
            "PDclock_channel": None
        }

        self.config.register_guild(**default_guild)
        self.config.register_user(**default_user)

    @commands.group(name="pdclock", autohelp=True)
    async def _pdclock(self, ctx: commands.Context):
        """
        PD clock-in commands
        """

    @_pdclock.command()
    @commands.guild_only()
    async def name(self, ctx: commands.Context, *,  name=None):
        """set your IC name for PD clock-in's."""
        if name:
            await self.config.user(ctx.author).name.set(name)
            await ctx.send("Your PD name has been set.")
        else:
            await self.config.user(ctx.author).name.set(name)
            await ctx.send("Your PD name has been removed.")

    @_pdclock.command()
    @commands.guild_only()
    async def channel(self, ctx, channel: discord.TextChannel = None):
        """Set the channel clockins get sent to."""
        if channel is None:
            await self.config.guild(ctx.guild).PDclock_channel.set(channel)
            await ctx.send("PD clock-in's has been disabled")
        else:
            await self.config.guild(ctx.guild).PDclock_channel.set(channel.id)
            await ctx.send(
                ("The PD clock-in's channel has been set to {channel.mention}").format(
                    channel=channel
                )
            )

    @commands.command()
    async def pdclockin(self, ctx: commands.Context):
        """
        clock into PD
        """
        channel_id = await self.config.guild(ctx.guild).PDclock_channel()
        if not channel_id:
            await ctx.send("The channel has not been set up to use this feature.")
        else:
            channel = ctx.guild.get_channel(channel_id)
        name = await self.config.user(ctx.author).name()
        if not name:
            name = ctx.author.display_name
        time = (datetime.datetime.utcnow() - datetime.timedelta(hours=4)).strftime('%Y%m%d')
        msg = await channel.send(f"**Name:** {name}/n **Clocked in:** {time} /n".format(name=name, time=time))
