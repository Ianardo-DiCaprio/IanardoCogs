import discord
from redbot.core import commands

Cog = getattr(commands, "Cog", object)
listener = getattr(Cog, "listener", lambda: lambda x: x)

class DirectM(Cog):



    async def allow_in_dm(self, ctx):
        """Checks if the bank is global and allows the command in dm"""
        if ctx.guild is None:
            return True

    @listener()
    async def on_message_without_command(self, ctx, message):
        if message.author.bot:
            return
        if await self.allow_in_dm(ctx):
            return await ctx.send("This is a test.")
			
