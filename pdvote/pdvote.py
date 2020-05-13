from typing import Any
from datetime import datetime
import asyncio
import discord

from redbot.core import Config, checks, commands
from redbot.core.bot import Red
from redbot.core.utils.predicates import MessagePredicate, ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.config import Config
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

        default_user = {"voted": False}
        default_guild = {"votee": None, "PDvote_channel": None, "PDmessage": None, "votemessage": None, "yes": 0, "no": 0}

        self.config.register_guild(**default_guild)
        self.config.register_user(**default_user)

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
        description = f"{user.mention} is being voted on for a promotion, use `]vote yes` or `]vote no` below."
        embed = discord.Embed(description=description, color=0x00FFFF)
        embed.set_author(name="PD Promotions")
        vote = await ctx.send(embed=embed)
        await self.config.guild(ctx.guild).votemessage.set(vote.id)

    @commands.command()
    @commands.guild_only()
    async def vote(self, ctx, vote: str):
        """If your vote isn't `yes` or `no` I'm going to kill you!"""
        votee_id = await self.config.guild(ctx.guild).votee()
        votee = ctx.guild.get_member(votee_id)
        if votee == ctx.author:
            await ctx.send("You cannot vote for yourself!")
            return
        channel_id = await self.config.guild(ctx.guild).PDvote_channel()
        channel = ctx.guild.get_channel(channel_id)
        yes = await self.config.guild(ctx.guild).yes()
        no = await self.config.guild(ctx.guild).no()
        if vote == "yes":
            yes = yes + 1
        if vote == "no":
            no = no + 1
            await self.config.user(ctx.author).voted.set(1)
        pdmessage = await self.config.guild(ctx.guild).PDmessage()
        voted = await self.config.user(ctx.author).voted()
        await self.config.user(ctx.author).voted.set(True)
        if voted:
            await ctx.send("You have already voted")
        else:
            if pdmessage is None:
                pdmessage = await channel.send(f"**{votee.display_name}:** **Yes:** {yes} | **No:** {no}")
                await self.config.guild(ctx.guild).PDmessage.set(pdmessage.id)
                await self.config.guild(ctx.guild).yes.set(yes)
                await self.config.guild(ctx.guild).no.set(no)
            else:
                pdmessage_id = await self.config.guild(ctx.guild).PDmessage()
                pdmessage = await channel.fetch_message(pdmessage_id)
                msg = f"**{votee.display_name}:** **Yes:** {yes} | **No:** {no}"
                await pdmessage.edit(content=msg)

    @commands.command()
    @commands.guild_only()
    async def resetvote(self, ctx):
        """If your vote isn't `yes` or `no` I'm going to kill you!"""
        await self.config.guild(ctx.guild).votemessage.set(None)
        await self.config.guild(ctx.guild).yes.set(0)
        await self.config.guild(ctx.guild).no.set(0)
        await self.config.guild(ctx.guild).PDmessage.set(None)
        for user in ctx.guild.members:
            await self.config.user(user).voted.set(False)
        await ctx.send("Voting has been reset!")
