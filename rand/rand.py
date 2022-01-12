import discord
import asyncio
import random
from redbot.core import commands, checks
import tekore as tk

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

    @commands.command(name="embed")
    async def embed(self, ctx: commands.Context):
        """this command sends a message"""
        embed=discord.Embed(title="PORN", url="https://www.pornhub.com/", description="This is porn", color=0x079de9)
        embed.set_author(name="Porn", url="http://therattgang.com/wp-content/uploads/2019/05/horny-pussy-during-sex.jpg", icon_url="http://therattgang.com/wp-content/uploads/2019/05/horny-pussy-during-sex.jpg")
        embed.set_thumbnail(url="http://therattgang.com/wp-content/uploads/2019/05/horny-pussy-during-sex.jpg")
        embed.set_image(url="http://therattgang.com/wp-content/uploads/2019/05/horny-pussy-during-sex.jpg")
        embed.add_field(name="Category 1", value="https://www.pornhub.com/categories/teen", inline=False)
        embed.add_field(name="Category 2", value="https://www.pornhub.com/categories/lesbian", inline=True)
        embed.set_footer(text="Do you like porn?")
        await ctx.send(embed=embed)

    @commands.command(name="spause")
    async def spause(self, ctx: commands.Context):
        """Pause Spotify"""
        conf = ("b29fcfa2b667421db65441fe8012f041", "9054ad8cf8614809a630ff4d91d99d4f", "https://example.com/callback")
        token = tk.prompt_for_user_token(conf, scope=tk.scope.every)

        spotify = tk.Spotify(token)
        tracks = spotify.current_user_top_tracks(limit=10)
        spotify.playback_start_tracks([t.id for t in tracks.items])
        


