from typing import Any
from datetime import datetime
import asyncio
import discord

from redbot.core import Config, checks, commands
from redbot.core.bot import Red
from redbot.core.utils.predicates import MessagePredicate, ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions
from datetime import datetime
from pytz import timezone

Cog: Any = getattr(commands, "Cog", object)


class PDVote(Cog):
    """
    Simple LFG commands
    """

    __author__ = "Ianardo DiCaprio"
    __version__ = "1.0.0"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, 699114013, force_registration=True)

        default_user = {"yes": 0, "no": 0, "PDmessage": None}
        default_guild = {"votee": None, "PDvote_channel": None}

        self.config.register_user(**default_user)
        self.config.register_guild(**default_guild)

    @commands.group(name="pdvotes", autohelp=True)
    async def _pdvotes(self, ctx: commands.Context):
        """
        PD vote commands
        """

    @_pdvotes.command()
    @commands.guild_only()
    async def channel(self, ctx, channel: discord.TextChannel = None):
        """Set the channel votes get sent to."""
        if channel is None:
            await self.config.guild(ctx.guild).PDvote_channel.set(channel)
            await ctx.send("Votes has been disabled")
        else:
            await self.config.guild(ctx.guild).PDvote_channel.set(channel.id)
            await ctx.send(
                ("The votes channel has been set to {channel.mention}").format(
                    channel=channel
                )
            )

    @commands.command()
    @commands.guild_only()
    async def pdvote(self, ctx, user: discord.Member = None):
        """Set who is being voted on."""
        await self.config.guild(ctx.guild).votee.set(user.id)
        description = f"{user.mention} is being voted on for a promotion, react below to cast your vote!"
        embed = discord.Embed(description=description, color=0x00FFFF)
        embed.set_author(name="PD Promotions")
        vote = await ctx.send(embed=embed)
        await self.config.PDmessage.set(vote.id)
        emoji = "✅"
        emoji2 = "❎"
        await vote.add_reaction(emoji)
        await vote.add_reaction(emoji2)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """on reactions"""
        channel = await self.bot.fetch_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        user = await self.bot.fetch_user(payload.user_id)
        emoji = payload.emoji
        if payload.emoji == "✅":
            await channel.send("yes")
        if payload.emoji == "❎":
            await channel.send("no")
