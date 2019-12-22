from typing import Any
from datetime import datetime
import asyncio
import discord

from redbot.core import Config, checks, commands
from redbot.core.bot import Red
from redbot.core.utils.predicates import MessagePredicate, ReactionPredicate
from redbot.core.utils.menus import start_adding_reactions

Cog: Any = getattr(commands, "Cog", object)


class LookingFG(Cog):
    """
    Simple LFG commands
    """

    __author__ = "Ianardo DiCaprio"
    __version__ = "1.0.0"

    def __init__(self, bot: Red):
        self.bot = bot
        self.config = Config.get_conf(self, 6991142013, force_registration=True)

        default_global = {"lfg_channel": None}

        self.config.register_global(**default_global)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def lfg(self, ctx: commands.Context):
        """Make an LFG request."""
        author = ctx.author
        bot = self.bot
        gamemode1 = bot.get_emoji(573299653613977601)
        expected = (gamemode1, "⏹", "⏯", "⏭")
        emoji = {"ones": f"{gamemode1}", "stop": "⏹", "pause": "⏯", "next": "⏭"}
        try:
            game = await author.send(
                "You have a maximum of 2 minutes to answer each question, "
                "Please specify what gamemode you are playing. eg: 3's"
            )
        except discord.Forbidden:
            return await ctx.send("I can't seem to be able to DM you. Do you have DM's closed?")

        message = await ctx.send("Okay, {0}, I've sent you a DM.".format(author.mention))

        def check(member):
            return member.author == author and member.channel == author.dm_channel

        try:
            task = start_adding_reactions(game, expected[:4], ctx.bot.loop)
            (r, u) = await bot.wait_for("reaction_add", timeout=120, check=ReactionPredicate.with_emojis(expected, game, ctx.author))
            reacts = {v: k for k, v in emoji.items()}
            react = reacts[r.emoji]
            if react == "ones":
                gamemode = "1's"
        except asyncio.TimeoutError:
            return await ctx.send("You took too long. Try again.")

        await author.send("What rank are you in this gamemode? e.g: Champion")
        try:
            rank = await bot.wait_for("message", timeout=120, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("You took too long. Try again.")

        await author.send("What servers are you playing on? e.g: EU, USE")
        try:
            server = await bot.wait_for("message", timeout=120, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("You took too long. Try again.")

        await author.send("What platform are you using? e.g: PC")
        try:
            platform = await bot.wait_for("message", timeout=120, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("You took too long. Try again.")

        await author.send("How many people are you looking for?")
        try:
            amount = await bot.wait_for("message", timeout=120, check=check)
        except asyncio.TimeoutError:
            return await ctx.send("You took too long. Try again.")

        embed = discord.Embed(color=await ctx.embed_colour(), timestamp=datetime.now())
        embed.set_author(name=f"{ctx.author.name} is looking for a Rocket League group", icon_url=author.avatar_url)
        embed.set_footer(text="{0}#{1} ({2})".format(author.name, author.discriminator, author.id))
        embed.add_field(name="GameMode:", value=gamemode, inline=True)
        embed.add_field(name="Rank:", value=rank.content, inline=True)
        embed.add_field(name="Server/s:", value=server.content, inline=True)
        embed.add_field(name="Platform:", value=platform.content, inline=True)
        embed.add_field(name="Looking for amount:", value=amount.content, inline=True)
        await message.delete()

        try:
            if await self.config.lfg_channel() is None:
                await author.send("It apprears that this hasn't been set up correctly on this server")
            else:
                channel = self.bot.get_channel(await self.config.lfg_channel())
                await channel.send(embed=embed)
                await author.send(
                    "Your LFG request has been made!"
                )
        except discord.Forbidden:
            await author.send("That didn't work for some reason")

    @checks.is_owner()
    @commands.guild_only()
    @commands.command()
    async def lfgsetup(
            self, ctx: commands.Context, channel: discord.TextChannel = None
        ):
        """Set the channel lfgrequests get sent to."""
        if channel is None:
            await self.config.lfg_channel.set(channel)
            await ctx.send("LFG has been disabled")
        else:
            await self.config.lfg_channel.set(channel.id)
            await ctx.send(
                ("The LFG channel has been set to {channel.mention}").format(
                    channel=channel
                )
            )
