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
            "message": None,
            "messageid": None,
            "admessageid": None,
            "count": 0,
            "weekcount": 0
        }
        default_guild = {
            "PDclock_channel": None,
            "adPDclock_channel": None
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

    @_pdclock.command()
    @commands.guild_only()
    async def adchannel(self, ctx, channel: discord.TextChannel = None):
        """Set the channel admin clockins get sent to"""
        if channel is None:
            await self.config.guild(ctx.guild).adPDclock_channel.set(channel)
            await ctx.send("PD clock-in's has been disabled")
        else:
            await self.config.guild(ctx.guild).adPDclock_channel.set(channel.id)
            await ctx.send(
                ("The PD clock-in's admin channel has been set to {channel.mention}").format(
                    channel=channel
                )
            )

    @_pdclock.command()
    @commands.guild_only()
    async def resetweek(self, ctx, count=0):
        """Reset weekly clock-in's"""
        for player in ctx.guild.members:
            await self.config.user(player).weekcount.set(count)
        await ctx.send("This weeks clock-in amounts have been reset")

    @commands.command()
    async def pdclockin(self, ctx: commands.Context):
        """
        clock into PD
        """
        channel_id = await self.config.guild(ctx.guild).PDclock_channel()
        adchannel_id = await self.config.guild(ctx.guild).adPDclock_channel()
        if not channel_id:
            await ctx.send("The channel has not been set up to use this feature.")
        else:
            channel = ctx.guild.get_channel(channel_id)
        if not adchannel_id:
            await ctx.send("The channel has not been set up to use this feature.")
        else:
            adchannel = ctx.guild.get_channel(adchannel_id)
        tz = timezone('EST5EDT')
        now = datetime.now(tz)
        time = now.strftime("%H:%M")
        authormention = ctx.author.display_name
        count = await self.config.user(ctx.author).count()
        weekcount = await self.config.user(ctx.author).weekcount()
        newcount = count + 1
        newweekcount = weekcount + 1
        await self.config.user(ctx.author).count.set(newcount)
        if count == 0:
            admsg = await adchannel.send(f"**Discord name:** {authormention}\n**Clocked in times:** {newcount}\n**Clock-in's this week:** {newweekcount}")
            await self.config.user(ctx.author).admessageid.set(admsg.id)
        else:
            adminmessage_id = await self.config.user(ctx.author).admessageid()
            admessageid = await adchannel.fetch_message(adminmessage_id)
            admsg = f"**Discord name:** {authormention}\n**Clocked in times:** {newcount}\n**Clock-in's this week:** {newweekcount}"
            await admessageid.edit(content=admsg)
        await self.config.user(ctx.author).count.set(newcount)
        await self.config.user(ctx.author).weekcount.set(newweekcount)
        msg = await channel.send(f"**Discord name:** {authormention}\n**Clocked in:** {time}\n")
        await self.config.user(ctx.author).message.set(msg.content)
        await self.config.user(ctx.author).messageid.set(msg.id)

    @commands.command()
    async def pdclockout(self, ctx: commands.Context):
        """
        clock out of PD
        """
        message = await self.config.user(ctx.author).message()
        message_id = await self.config.user(ctx.author).messageid()
        channel_id = await self.config.guild(ctx.guild).PDclock_channel()
        channel = ctx.guild.get_channel(channel_id)
        tz = timezone('EST5EDT')
        now = datetime.now(tz)
        time = now.strftime("%H:%M")
        new_message = message + f"\n**Clocked out:** {time}".format(time=time)
        messageid = await channel.fetch_message(message_id)
        await messageid.edit(content=new_message)
        await self.config.user(ctx.author).message.set(None)
        await self.config.user(ctx.author).messageid.set(None)
