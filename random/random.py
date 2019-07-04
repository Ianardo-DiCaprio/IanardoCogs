import discord
from redbot.core import commands

class Random(commands.Cog):
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
        if an emoji in not specified it will react with
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
