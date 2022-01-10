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

    @commands.command(name="cum")
    async def cum(self, ctx: commands.Context):
        """this command sends a message"""
        a = random.randint(1, 4)
        if a == 1:
            message = "My cum is white and thick and shoots far."
        elif a == 2:
            message = "My cum is translucent and sprays"
        elif a == 3:
            message = "My cum doesn't shoot it drips"
        elif a == 4:
            message = "8======D ~~~~~~~"
        await ctx.send(message)
