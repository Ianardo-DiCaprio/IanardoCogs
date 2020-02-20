from redbot.core import Config
from datetime import datetime
import discord
import random


class MiddleManCore:
    def __init__(self, bot):
        self.bot = bot

        self.config = Config.get_conf(self, identifier=213443534287593)
        default_guild = {
            'category': None,
            'closed_category': None,
            'middleman_role': None,
            'default_message_middleman_channel': None,
            'sessions': {}
        }
        self.config.register_guild(**default_guild)

        self.middleman_info_format = '\n\n**[{datetime}]**[{membername}][{author}]\n{information}'

    async def create_middleman(self, context, membername):
        guild = context.guild
        author = context.author

        middleman_role = [role for role in guild.roles if await self.config.guild(guild).middleman_role() == role.id]

        if middleman_role:
            middleman_role = middleman_role[0]
        category_channel = await self.config.guild(guild).category()
        default_message_middleman_channel = await self.config.guild(guild).default_message_middleman_channel()

        if category_channel and category_channel in [category.id for category in guild.categories]:
            n1 = 10**10
            n2 = n1 * 10 - 1
            middleman_id = int(random.randint(n1, n2))
            middleman_channel = await guild.create_text_channel('{}-{}'.format(author.display_name, middleman_id),
                                                             category=self.bot.get_channel(category_channel))

            await middleman_channel.set_permissions(author, read_messages=True, send_messages=True)
            await middleman_channel.set_permissions(membername, read_messages=True, send_messages=True)
            await middleman_channel.set_permissions(guild.me, read_messages=True, send_messages=True, manage_channels=True)

            await middleman_channel.edit(topic=self.middleman_info_format.format(middleman=middleman_id,
                                      datetime=datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S'),
                                      membername="<@" + str(membername.id) + ">",
                                      author=author.display_name,
                                      information='Middleman opened'))

            if default_message_middleman_channel:
                await middleman_channel.send(default_message_middleman_channel.format(member=author,
                                                                                channel=middleman_channel,
                                                                                origin=context.channel,
                                                                                middleman_role=middleman_role))

            async with self.config.guild(guild).sessions() as session:
                    session.update({middleman_channel.id: author.id})

        else:
            return 'You need to run the setup first.'

    async def update_middleman(self, context, status):
        try:
            await context.message.delete()
        except discord.Forbidden:
            pass

        guild = context.guild
        channel = context.channel
        author = context.author

        sessions = await self.config.guild(guild).sessions()

        if str(channel.id) in sessions and await self.config.guild(guild).middleman_role() in [role.id for role in author.roles]:

            middleman_id = str(channel.name).split('-')[1]
            await channel.edit(topic=channel.topic+self.middleman_info_format.format(
                                middleman=middleman_id,
                                datetime=datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S'),
                                author=author.display_name,
                                information=status)
                               )

    async def close_middleman(self, context, membername):
        try:
            await context.message.delete()
        except discord.Forbidden:
            pass

        guild = context.guild
        channel = context.channel
        author = context.author

        sessions = await self.config.guild(guild).sessions()

        if str(channel.id) in sessions and await self.config.guild(guild).middleman_role() in [role.id for role in author.roles]:

            member = guild.get_member(sessions[str(channel.id)])
            middleman_id = str(channel.name).split('-')[1]

            closed_category = await self.config.guild(guild).closed_category()
            closed_category = self.bot.get_channel(closed_category)

            await channel.set_permissions(member, read_messages=True, send_messages=False)
            await channel.set_permissions(membername, read_messages=True, send_messages=False)
            await channel.edit(category=closed_category,
                               topic=channel.topic+self.middleman_info_format.format(
                                    middleman= "",
                                    datetime=datetime.utcnow().strftime('%d/%m/%Y %H:%M:%S'),
                                    membername=membername.id,
                                    author=author.display_name,
                                    information='Middleman closed'))

            async with self.config.guild(guild).sessions() as session:
                    session.pop(channel.id, None)

    async def purge_middleman(self, context):
        try:
            guild = context.guild
            closed_channels = [channel for channel in guild.channels if channel.category_id == await self.config.guild(guild).closed_category()]
            for channel in closed_channels:
                await channel.delete()

            return 'All closed middleman channels removed!'
        except discord.Forbidden:
            return 'I need permissions to manage channels.'

    async def set_default_message_middleman_channel(self, context, message):
        guild = context.guild

        await self.config.guild(guild).default_message_middleman_channel.set(message)

        return 'Your default message has been set.'

    async def automatic_setup(self, context):
        guild = context.guild

        try:
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(send_messages=False, read_messages=False),
            }

            category_channel = await guild.create_category('Middleman', overwrites=overwrites)
            closed_category_channel = await guild.create_category('Closed Middleman', overwrites=overwrites)

            middleman_role = await guild.create_role(name='Middleman')

            await category_channel.set_permissions(middleman_role, read_messages=True, send_messages=True)
            await closed_category_channel.set_permissions(middleman_role, read_messages=True, send_messages=True)

            await self.config.guild(guild).category.set(category_channel.id)
            await self.config.guild(guild).closed_category.set(closed_category_channel.id)
            await self.config.guild(guild).middleman_role.set(middleman_role.id)

            return 'You\'re all done! Now add the `Middleman` role to anyone who you deem good enough to handle trades.'
        except discord.Forbidden:
            return 'That didn\'t go well... I need permissions to manage channels and manage roles. :rolling_eyes:'
