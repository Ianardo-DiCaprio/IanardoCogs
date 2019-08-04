from typing import Any
from datetime import datetime
import asyncio
import discord

from redbot.core import Config, checks, commands
from redbot.core.bot import Red

Cog: Any = getattr(commands, "Cog", object)


class BugReport(Cog):
    """
    Simple Bug Reporting cog
    """

    __author__ = "Ianardo DiCaprio"
    __version__ = "1.0.0"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, 6991142013, force_registration=True)

        default_global = {"report_channel": None}

        self.config.register_global(**default_global)

    @commands.command()
    @commands.cooldown(rate=1, per=300, type=commands.BucketType.user)
    async def reportbug(self, ctx: commands.Context):
        """Report a bug."""
        author = ctx.author
        bot = self.bot
        try:
            await author.send(
                "You have a maximum of 2 minutes to answer each question, "
                "Please write a brief description of your bug."
            )
        except discord.Forbidden:
            return await ctx.send("I can't seem to be able to DM you. Do you have DM's closed?")

        await ctx.send("Okay, {0}, I've sent you a DM.".format(author.mention))

        def check(member):
            return member.author == author and member.channel == author.dm_channel

        try:
            description = await bot.wait_for("message", timeout=120, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("You took too long. Try again.")

        await author.send("What steps are needed to reproduce this bug? (Send them in 1 message)")
        try:
            repro = await bot.wait_for("message", timeout=120, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("You took too long. Try again.")

        await author.send("What command(s) does this bug happen on?")
        try:
            command = await bot.wait_for("message", timeout=120, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("You took too long. Try again.")

        await author.send("What is supposed to happen?")
        try:
            supposed = await bot.wait_for("message", timeout=120, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("You took too long. Try again.")

        await author.send("What actually happened?")
        try:
            happened = await bot.wait_for("message", timeout=120, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("You took too long. Try again.")

        await author.send("What platform are you on?")
        try:
            platform = await bot.wait_for("message", timeout=120, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("You took too long. Try again.")

        embed = discord.Embed(color=await ctx.embed_colour(), timestamp=datetime.now())
        embed.set_author(name="New Bug Report!", icon_url=author.avatar_url)
        embed.set_footer(text="{0}#{1} ({2})".format(author.name, author.discriminator, author.id))
        embed.title = "User: {0}#{1} ({2})".format(author.name, author.discriminator, author.id)
        embed.add_field(name="Description:", value=description.content, inline=False)
        embed.add_field(name="Reproduction Steps:", value=repro.content, inline=False)
        embed.add_field(name="Command(s) with issue:", value=command.content, inline=False)
        embed.add_field(name="What's supposed to happen:", value=supposed.content, inline=False)
        embed.add_field(name="What actually happened:", value=happened.content, inline=False)
        embed.add_field(name="Platform:", value=platform.content, inline=False)

        try:
            if await self.config.report_channel() is None:
                await bot.send_to_owners(embed=embed)
                botowner = bot.owner_id
                bots = bot.get_user(botowner)
                await bot.send_to_owners(bots.mention)
            elif await self.config.report_channel() == "owner":
                await bot.send_to_owners(embed=embed)
                botowner = bot.owner_id
                bots = bot.get_user(botowner)
                await bot.send_to_owners(bots.mention)
            else:
                channel = self.bot.get_channel(await self.config.report_channel())
                await channel.send(embed=embed)
                botowner = bot.owner_id
                bots = bot.get_user(botowner)
                await channel.send(bots.mention)
                await author.send(
                    "Your bug report has been sent to the owner and you will "
                    "recieve a message shortly. thank you!"
                )
        except discord.Forbidden:
            await author.send("That didn't work for some reason")

    @checks.is_owner()
    @commands.command()
    async def bugsetup(
            self, ctx: commands.Context, channel: discord.TextChannel = None, owner=None
        ):
        """Set the channel bug reports get sent to."""
        if channel is None:
            owner == "owner"
            await self.config.report_channel.set(owner)
            await ctx.send("Bug reports will now be sent to the owners DM's")
        else:
            await self.config.report_channel.set(channel.id)
            await ctx.send(
                ("The bug report channel has been set to {channel.mention}").format(
                    channel=channel
                )
            )

    @checks.is_owner()
    @commands.command()
    async def fixed(self, ctx: commands.Context, target: discord.Member):
        """Mark a report as fixed."""
        await ctx.send("Bug report fixed sent to {}.".format(target.mention))
        await target.send("The bug you reported has been fixed, thank you for the report.")

    @checks.is_owner()
    @commands.command()
    async def nobug(self, ctx: commands.Context, target: discord.Member):
        """Do if a bug report isn't a bug"""
        await ctx.send("No bug sent to {}.".format(target.mention))
        await target.send(
            "The bug you reported isn't a bug. Please use `]contact` if you still need help."
        )
