import discord
import asyncio
import random
from redbot.core import commands, checks

class Rand(commands.Cog):
    """
    Simple random cog
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="isjarigay")
    @commands.cooldown(rate=1, per=3, type= commands.BucketType.user)
    async def sendmessage(self, ctx: commands.Context):
        """this command sends a message"""
        a = random.randint(1, 2)
        if a == 1:
            message = "Jari is gay!"
        elif a == 2:
            message = "You're not gay for now."
        await ctx.send(message)
    
    
