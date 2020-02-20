from redbot.core import commands
from .core import MiddleManCore

import discord

BaseCog = getattr(commands, "Cog", object)

class MiddleMan(BaseCog):
    def __init__(self, bot):
        self.bot = bot
        self.core = MiddleManCore(bot)

    @commands.group(name='middleman')
    async def middleman(self, context):
        '''
        Middleman trades!
        '''

    @middleman.command(name='new')
    async def middleman_new(self, context, membername: discord.Member = None):
        '''
        Create a new middleman channel.
        '''
        if not membername:
            await context.send("Please mention a user you want to trade with")
            return
        if context.invoked_subcommand is None:
            message = await self.core.create_middleman(context, membername)
            if message:
                await context.send(message)

    @middleman.command(name='update')
    async def middleman_update(self, context, *, status: str):
        '''
        Update the status of a middleman trade.
        '''
        await self.core.update_middleman(context, status)

    @middleman.command(name='close')
    async def middleman_close(self, context, membername: discord.Member = None):
        '''
        Close a middleman channel.
        '''
        if not membername:
            await context.send("Please mention the user that is mentioned in the channel topic. Eg: [middleman close @user")
            return
        await self.core.close_middleman(context, membername)

    @middleman.group(name='set')
    @commands.has_permissions(administrator=True)
    async def middleman_set(self, context):
        '''
        Settings
        '''

    @middleman_set.command(name='purge')
    async def middleman_set_purge(self, context):
        '''
        Delete all closed middleman channels.
        '''
        message = await self.core.purge_middleman(context)
        await context.send(message)

    @middleman_set.command(name='message')
    @commands.has_permissions(administrator=True)
    async def middleman_set_message(self, context, *, message: str):
        '''
        Set the default message when a new middleman channel has been created (markdown safe)
        '''
        message = await self.core.set_default_message_middleman_channel(context, message)
        await context.send(message)

    @middleman_set.command(name='setup')
    async def middleman_setup(self, context):
        '''
        Automatic setup
        '''
        message = await self.core.automatic_setup(context)
        await context.send(message)
