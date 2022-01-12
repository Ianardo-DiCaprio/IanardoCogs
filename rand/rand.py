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
        token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)

        spotify = tk.Spotify(token)
        tracks = spotify.current_user_top_tracks(limit=10)
        spotify.playback_start_tracks([t.id for t in tracks.items])
        tracks = spotify.current_user_top_tracks(limit=10)
        for track in tracks.items:
            await ctx.send(track.name)

    @commands.command(name="salbum")
    async def salbum(self, ctx: commands.Context, *, query: str = None):
        """Pause Spotify"""
        conf = ("b29fcfa2b667421db65441fe8012f041", "9054ad8cf8614809a630ff4d91d99d4f", "https://example.com/callback")
        token = tk.prompt_for_user_token(*conf, scope=tk.scope.every)

        spotify = tk.Spotify(token)
        if query is None:
            await ctx.send("No search query specified")
            return

        tracks, = spotify.search(query, limit=5)
        embed = discord.Embed(title="Track search results", color=0x1DB954)
        embed.set_thumbnail(url="https://i.imgur.com/890YSn2.png")
        embed.set_footer(text="Requested by " + ctx.author.display_name)

        for t in tracks.items:
            artist = t.artists[0].name
            url = t.external_urls["spotify"]

            message = "\n".join([
                "[Spotify](" + url + ")",
                ":busts_in_silhouette: " + artist,
                ":cd: " + t.album.name
            ])
            embed.add_field(name=t.name, value=message, inline=False)
            spotify.playback_start_tracks([t.id for t in tracks.items])

        await ctx.send(embed=embed)
