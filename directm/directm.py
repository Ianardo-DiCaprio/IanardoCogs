import discord
from redbot.core import commands


class DirectM(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_without_command(self, ctx):
        if ctx.guild is None:
            channel = ctx.channel
            return await channel.send("This command is not available in DM's on this bot.")
			
