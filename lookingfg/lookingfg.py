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
        gamemode1 = bot.get_emoji(971907439408603186)
        gamemode2 = bot.get_emoji(971907549668458566)
        gamemode3 = bot.get_emoji(971907579863257099)
        gamemodeo = bot.get_emoji(971907603049381889)
        rank1 = bot.get_emoji(658431823935832064)
        rank2 = bot.get_emoji(658431824342548510)
        rank3 = bot.get_emoji(658431823746957313)
        rank4 = bot.get_emoji(658431824279896064)
        rank5 = bot.get_emoji(658431824065986562)
        rank6 = bot.get_emoji(658431823931506710)
        rank7 = bot.get_emoji(658431823608545294)
        region1 = bot.get_emoji(658435948513722399)
        region2 = bot.get_emoji(658435948572442635)
        region3 = bot.get_emoji(658435948425641994)
        region4 = bot.get_emoji(658435948492750869)
        region5 = bot.get_emoji(658435948236767236)
        region6 = bot.get_emoji(658435948631162880)
        region7 = bot.get_emoji(658435948211601422)
        region8 = bot.get_emoji(658435948589088787)
        region9 = bot.get_emoji(658435948610191366)
        region10 = bot.get_emoji(658435948983353377)
        platform1 = bot.get_emoji(658438656826015775)
        platform2 = bot.get_emoji(658438656570294314)
        platform3 = bot.get_emoji(658438656872415262)
        platform4 = bot.get_emoji(658438656863895562)
        gamemodes = (gamemode1, gamemode2, gamemode3, gamemodeo)
        gamemodeemoji = {"ones": gamemode1, "twos": gamemode2, "threes": gamemode3, "other": gamemodeo}
        ranks = (rank1, rank2, rank3, rank4, rank5, rank6, rank7)
        rankemoji = {"bronze": rank1, "silver": rank2, "gold": rank3, "platinum": rank4, "diamond": rank5, "champion": rank6, "grandchampion": rank7}
        regions = (region1, region2, region3, region4, region5, region6, region7, region8, region9, region10)
        regionemoji = {"usw": region1, "use": region2, "sam": region3, "saf": region4, "oce": region5, "me": region6, "jpn": region7, "eu": region8, "asm": region9, "asc": region10}
        platforms = (platform1, platform2, platform3, platform4)
        platformemoji = {"pc": platform1, "xbox": platform2, "ps": platform3, "switch": platform4}
        players = ("1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣")
        playeremoji = {"1": "1️⃣", "2": "2️⃣", "3": "3️⃣", "4": "4️⃣", "5": "5️⃣", "6": "6️⃣", "7": "7️⃣"}
        try:
            game = await author.send(
                "**You have a maximum of 2 minutes to answer each question, "
                "Please specify what gamemode you are playing.**"
            )
        except discord.Forbidden:
            return await ctx.send("I can't seem to be able to DM you. Do you have DM's closed?")

        message = await ctx.send("Okay, {0}, I've sent you a DM.".format(author.mention))
        try:
            task = start_adding_reactions(game, gamemodes[:4])
            (r, u) = await bot.wait_for("reaction_add", timeout=120, check=ReactionPredicate.with_emojis(gamemodes, game, ctx.author))
            reacts = {v: k for k, v in gamemodeemoji.items()}
            react = reacts[r.emoji]
            if react == "ones":
                gamemode = "1's"
            elif react == "twos":
                gamemode = "2's"
            elif react == "threes":
                gamemode = "3's"
            elif react == "other":
                gamemode = "Other"
        except asyncio.TimeoutError:
            return await author.send("You took too long. Try again.")

        rank = await author.send("**What rank are you in this gamemode?**")
        try:
            task = start_adding_reactions(rank, ranks[:7], ctx.bot.loop)
            (r, u) = await bot.wait_for("reaction_add", timeout=120, check=ReactionPredicate.with_emojis(ranks, rank, ctx.author))
            reacts = {v: k for k, v in rankemoji.items()}
            react = reacts[r.emoji]
            if react == "bronze":
                rank = "Bronze"
            elif react == "silver":
                rank = "Silver"
            elif react == "gold":
                rank = "Gold"
            elif react == "platinum":
                rank = "Platinum"
            elif react == "diamond":
                rank = "Diamond"
            elif react == "champion":
                rank = "Champion"
            elif react == "grandchampion":
                rank = "Grand Champion"
        except asyncio.TimeoutError:
            return await author.send("You took too long. Try again.")

        region = await author.send("**What servers are you playing on?**")
        try:
            task = start_adding_reactions(region, regions[:10], ctx.bot.loop)
            (r, u) = await bot.wait_for("reaction_add", timeout=120, check=ReactionPredicate.with_emojis(regions, region, ctx.author))
            reacts = {v: k for k, v in regionemoji.items()}
            react = reacts[r.emoji]
            if react == "usw":
                region = "US-West"
            elif react == "use":
                region = "US-East"
            elif react == "sam":
                region = "South America"
            elif react == "saf":
                region = "South African"
            elif react == "oce":
                region = "Oceana"
            elif react == "me":
                region = "Middle East"
            elif react == "jpn":
                region = "Japan"
            elif react == "eu":
                region = "Europe"
            elif react == "asm":
                region = "Asia Mainlane"
            elif react == "asc":
                region = "Asia East"
        except asyncio.TimeoutError:
            return await author.send("You took too long. Try again.")

        platform = await author.send("**What platform are you using?**")
        try:
            task = start_adding_reactions(platform, platforms[:4], ctx.bot.loop)
            (r, u) = await bot.wait_for("reaction_add", timeout=120, check=ReactionPredicate.with_emojis(platforms, platform, ctx.author))
            reacts = {v: k for k, v in platformemoji.items()}
            react = reacts[r.emoji]
            if react == "pc":
                platform = "PC"
            elif react == "xbox":
                platform = "Xbox"
            elif react == "ps":
                platform = "PlayStation"
            elif react == "switch":
                platform = "Nintendo Switch"
        except asyncio.TimeoutError:
            return await author.send("You took too long. Try again.")

        player = await author.send("**How many people are you looking for?**")
        try:
            task = start_adding_reactions(player, players[:7], ctx.bot.loop)
            (r, u) = await bot.wait_for("reaction_add", timeout=120, check=ReactionPredicate.with_emojis(players, player, ctx.author))
            reacts = {v: k for k, v in playeremoji.items()}
            react = reacts[r.emoji]
            if react == "1":
                player = "1"
            elif react == "2":
                player = "2"
            elif react == "3":
                player = "3"
            elif react == "4":
                player = "4"
            elif react == "5":
                player = "5"
            elif react == "6":
                player = "6"
            elif react == "7":
                player = "7"
        except asyncio.TimeoutError:
            return await author.send("You took too long. Try again.")

        embed = discord.Embed(color=await ctx.embed_colour(), timestamp=datetime.now())
        embed.set_author(name=f"{ctx.author.name} is looking for a Rocket League group", icon_url=author.avatar_url)
        embed.set_footer(text="{0}#{1} ({2})".format(author.name, author.discriminator, author.id))
        embed.add_field(name="GameMode:", value=gamemode, inline=True)
        embed.add_field(name="Rank:", value=rank, inline=True)
        embed.add_field(name="Server:", value=region, inline=True)
        embed.add_field(name="Platform:", value=platform, inline=True)
        embed.add_field(name="Looking for:", value=player, inline=True)
        await message.delete()

        try:
            if await self.config.lfg_channel() is None:
                await author.send("It apprears that this hasn't been set up correctly on this server")
            else:
                channel = self.bot.get_channel(await self.config.lfg_channel())
                please = await channel.send(embed=embed)
                await author.send(
                    "**Your LFG request has been made!**"
                )
                await asyncio.sleep(1800)
                await please.delete()
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
