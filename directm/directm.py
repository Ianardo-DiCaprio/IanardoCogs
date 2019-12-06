import discord
from redbot.core import commands


class DirectM(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_without_command(self, ctx):
        if ctx.author.bot:
            return
        if ctx.guild is None:
            channel = ctx.channel
            await channel.send("**How to get support**\n"
                "Follow these steps! \n"
                "Type `[ticket new` In the channel that is created ask your question"
                "and a mod will be there to help you shortly :slight_smile:")
			
