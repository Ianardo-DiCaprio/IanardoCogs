import discord
from redbot.core import commands


class DirectM(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def allow_in_dm(self, ctx):
        """Checks if the bank is global and allows the command in dm"""
        if ctx.guild is None:
            return True

    @commands.Cog.listener()
    async def on_message_without_command(self, ctx, message):
        if message.author.bot:
            return
        if await self.allow_in_dm(ctx):
            return await ctx.send("This is a test.")
			
