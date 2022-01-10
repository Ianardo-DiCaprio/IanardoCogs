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
    @commands.cooldown(rate=1, per=3, type= commands.BucketType.user)
    async def sendmessage(self, ctx: commands.Context, text: str = ""):
        """this command sends a message"""
        if text == "":
            message = "There is nothing here"
        if text == "help":
            message = "Help me stepbro."
        else:
            message = "Well that's not an option."
        await ctx.send(message)
    
    
