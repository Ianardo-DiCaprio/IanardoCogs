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
            "role": None,
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
    async def autolog_channel(self, ctx, *, channel: discord.TextChannel = None):
        """Change the channel to which the bot checks for specific values."""
        if channel:
            await self.config.guild(ctx.guild).channel.set(channel.id)
            await ctx.send(("The channel has been set to {channel.mention}").format(channel=channel))

    @_checklog.command(name="role")
    @commands.guild_only()
    @checks.guildowner_or_permissions(administrator=True)
    async def autolog_channel(self, ctx, *, role: discord.Role = None):
        """Change the role to which the bot mentions when specific values are exceeded."""
        if role:
            await self.config.guild(ctx.guild).role.set(role.id)
            await ctx.send(("The role has been set to <@{role}>").format(role=role.id))

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """Please?"""
        channel = await self.config.guild(message.guild).channel()
        if message.channel.id == channel:
            replaced = message.content.replace("$", " ")
            await message.channel.send("Replaced")
            newmessage = [int(s) for s in replaced.split() if s.isdigit()]
            await message.channel.send("Split")
            newermessage = str(newmessage).strip('[]')
            await message.channel.send("Stripped")
            if int(newermessage) > 500000:
                await message.channel.send("More Than")
                role = await self.config.guild(message.guild).role()
                await message.channel.send("WOO")
