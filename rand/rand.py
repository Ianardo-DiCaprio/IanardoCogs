import discord
import asyncio
from redbot.core import commands, checks

class Rand(commands.Cog):
    """
    Simple random cog
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(rate=1, per=3, type=commands.BucketType.user)
    async def reaction(
        self, ctx: commands.Context, msg_id: int, emoji = None, channel: discord.TextChannel = None
    ):
        """React to a message.\n
	Msg_id is the message ID you want to react to. 
        If a channel is not specified it will look for
        the message ID in the current channel.
        If an emoji in not specified it will react with
        a "✅". If you wish to specify a channel, you 
        must also specify an emoji.
        """
        if not channel:
            channel = ctx.channel
        if not emoji:
            emoji = "✅"
        try:
            msg = await channel.fetch_message(msg_id)
            await msg.add_reaction(emoji)
        except discord.HTTPException:
            await ctx.send(
                "That message ID isn't in this channel, please specify the channel the message is in or use the correct message ID."
            )

    @commands.command(name="s")
    @checks.is_owner()
    async def say(self, ctx, *, text: str = ""):
        """Make the bot say something and delete the command
        that was used to make the bot say something."""
        if text != "":
            try:
                msg = await ctx.send(text)
                await ctx.message.delete()
            except:
                print("Can't be used in DMs")
        else:
            await ctx.send("Please include some text for me to say")

    @commands.command()
    @commands.guild_only()
    async def reacted(self, ctx, msg_id):
        """See who reacted to a message"""
        channel = ctx.channel
        msg = await channel.fetch_message(msg_id)
        new_msg = ""
        for reaction in msg.reactions:
            async for user in reaction.users():
                new_msg += "```{}#{} {}\n```".format(user.name, user.discriminator, reaction.emoji)
                embed = discord.Embed(title="Reactions", description=new_msg, color=0x404040)
                await ctx.send(embed)
