import asyncio
import discord
from redbot.core import commands, checks, Config

class CheckLog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self, identifier=34645634465834, force_registration=True
        )

        default_guild = {
            "channel": None,
        }

        self.config.register_guild(**default_guild)

    @commands.group(name="checklog", autohelp=True)
    async def _checklog(self, ctx: commands.Context):
        """
        CheckLog commands
        """
    @_checklog.command(name="channel")
    @commands.guild_only()
    @checks.guildowner_or_permissions(administrator=True)
    async def channel(self, ctx, *, channel: discord.TextChannel = None):
        """Change the channel to which the bot checks for specific values."""
        if channel:
            await self.config.guild(ctx.guild).channel.set(channel.id)
            await ctx.send(("The channel has been set to {channel.mention}").format(channel=channel))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """Please?"""
        channel = await self.config.guild(message.guild).channel()
        if message.channel.id == channel:
            replaced = message.content.replace("$", " ")
            newmessage = [int(s) for s in replaced.split() if s.isdigit()]
            newermessage = str(newmessage).strip('[]')
            try:
                if int(newermessage) > 500000:
                    await message.channel.send(f"<@&689100532690059274>")
            except:
                if "AP pistol" in message.content:
                    await message.channel.send(f"<@&689100532690059274>")
