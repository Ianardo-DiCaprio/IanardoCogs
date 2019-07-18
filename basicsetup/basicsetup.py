import asyncio
import discord

from redbot.core import commands, checks
from redbot.core.utils.chat_formatting import box
from redbot.core.utils.predicates import MessagePredicate
from discord.ext.commands import TextChannelConverter

BaseCog = getattr(commands, "Cog", object)

class BasicSetup(BaseCog):
    """Basic setup commands"""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        """Use this for help with setting 
        up basic commands when adding this 
        bot to a new server"""

        await ctx.send("**I will now ask you several questions which you need to answer. You have 60 seconds to answer each question before the next question is asked.**")
        await asyncio.sleep(1)
        await self.basic_setup(ctx)

    async def basic_setup(self, ctx):
        predicate = MessagePredicate.yes_or_no(ctx, ctx.channel, ctx.author)
        predicate1 = MessagePredicate.greater(0, ctx, ctx.channel, ctx.author)
        predicate2 = MessagePredicate.length_less(200, ctx, ctx.channel, ctx.author)
        predicate3 = MessagePredicate.length_less(200, ctx, ctx.channel, discord.Role)
        

        q1 = "Would you like to setup Anti Mention Spam?"
        q2 = "Would you like the user to be banned when exceeding the max mentions?"
        q3 = "Would you like to setup timed mention spam? (mentions from multiple messages in a set time)"
        q4 = "Would you like to setup an automatic role when a user joins?"
        q5 = "Would you like to setup bancheck, which checks new users against several databases to see if they have been banned?"
        q6 = "Would you like to set up the bots bank settings?"
        q7 = "Would you like to set up logs for things that happen in the server?"
        q8 = "Would you like to change the name of the casino?"
        q9 = "Would you like the bot to respond to messages when the bot is mentioned at the start of the message?"
        q10 = "Would you like to setup the dungeon?"
        q11 = "Would you like to setup the economy settings?"
        q12 = "Would you like to setup filtered words?"
        q13 = "Would you like to add a channel that shows the amount of users in the server?"
        q14 = "Would you like to add a channel that recieves a message when a user leaves the server?"
        q15 = "Would you like a channel for recieving lyrics when using the lyrics command?"
        q16 = "Would you like to setup basic auto mod features?"
        q17 = "Would you like to setup a mod log?"
        q18 = "Would you like to setup reports?"
        q19 = "Would you like to setup starboard?"
        q20 = "Would you like to setup tickets?"
        q21 = "Would you like to setup a welcome message for new users?"
        q22 = "Would you like to setup the mod and admin role?"
        q23 = "Would you like to setup reaction roles?"

        try:
            cog = self.bot.get_cog("AntiMentionSpam")
            if cog:
                if await self._get_response(ctx, q1, predicate) == 'yes':
                    number = await self._get_response(ctx, "How many mentions from a single user in a single message should be acted upon?", predicate1)
                    number = int(number)
                    await ctx.invoke(ctx.bot.get_command("antimentionspam max"), number)
                    await asyncio.sleep(1)
                    await self._get_response(ctx, q2, predicate) == 'yes'
                    await ctx.invoke(ctx.bot.get_command("antimentionspam autobantoggle"))
                    await asyncio.sleep(1)
                    await self._get_response(ctx, q3, predicate) == 'yes'
                    number = int(await self._get_response(ctx, "How many mentions?", predicate1))
                    await asyncio.sleep(0.5)
                    number1 = int(await self._get_response(ctx, "In how many seconds?", predicate1))
                    await ctx.invoke(ctx.bot.get_command("antimentionspam  maxinterval"), number, number1)
                    await asyncio.sleep(1)
        except asyncio.TimeoutError:
            pass
        try:
            cog = self.bot.get_cog("Autorole")
            if cog:
                if await self._get_response(ctx, q4, predicate) == 'yes':
                    await ctx.invoke(ctx.bot.get_command("autorole toggle"))
                    await asyncio.sleep(1)
                    rolemessage = await self._get_response(ctx, "What role would you like to be added to new users?", predicate2)
                    role = await commands.RoleConverter().convert(ctx, rolemessage)
                    await ctx.invoke(ctx.bot.get_command("autorole add"), role=role)
                    await asyncio.sleep(1)
        except asyncio.TimeoutError:
            pass
        try:
            cog = self.bot.get_cog("BanCheck")
            if cog:
                if await self._get_response(ctx, q5, predicate) == 'yes':
                    channelmessage = await self._get_response(ctx, "What channel would you like to be used as log?", predicate2)
                    channel = await (TextChannelConverter()).convert(ctx, channelmessage)
                    await ctx.invoke(ctx.bot.get_command("bancheckset enablechannel"), channel)
                    await asyncio.sleep(1)
        except asyncio.TimeoutError:
            pass
        try:
            cog = self.bot.get_cog("Bank")
            if cog:
                if await self._get_response(ctx, q6, predicate) == 'yes':
                    name = await self._get_response(ctx, "What would you like the bank to be called?", predicate2)
                    await ctx.invoke(ctx.bot.get_command("bankset bankname"), name=name)
                    await asyncio.sleep(1)
                    name1 = await self._get_response(ctx, "What would you like the credits to be called?", predicate2)
                    await ctx.invoke(ctx.bot.get_command("bankset creditsname"), name=name1)
                    await asyncio.sleep(1)
        except asyncio.TimeoutError:
            pass
        try:
            cog = self.bot.get_cog("Grenzpolizei")
            if cog:
                if await self._get_response(ctx, q7, predicate) == 'yes':
                    await ctx.invoke(ctx.bot.get_command("gp autosetup"))
                    await asyncio.sleep(1)
        except asyncio.TimeoutError:
            pass
        try:
            cog = self.bot.get_cog("Casino")
            if cog:
                if await self._get_response(ctx, q8, predicate) == 'yes':
                    name = await self._get_response(ctx, "What would you like the casino to be called?", predicate2)
                    await ctx.invoke(ctx.bot.get_command("casinoset name"), name=name)
                    await asyncio.sleep(1)
        except asyncio.TimeoutError:
            pass
        try:
            cog = self.bot.get_cog("CleverBot")
            if cog:
                if await self._get_response(ctx, q9, predicate) == 'yes':
                    await ctx.invoke(ctx.bot.get_command("cleverbotset toggle"))
                    await asyncio.sleep(1)
        except asyncio.TimeoutError:
            pass
        try:
            cog = self.bot.get_cog("Dungeon")
            if cog:
                if await self._get_response(ctx, q10, predicate) == 'yes':
                    await ctx.invoke(ctx.bot.get_command("dungeon toggle"))
                    await asyncio.sleep(0.5)
                    await ctx.invoke(ctx.bot.get_command("dungeon autoban"))
                    await asyncio.sleep(1)
                    days = await self._get_response(ctx, "How many days old must an account be before I automatically ban them?", predicate1)
                    await ctx.invoke(ctx.bot.get_command("dungeon joindays"), days=days)
                    await asyncio.sleep(1)
                    ans = await self._get_response(ctx, "Would you like users with default profile pics to be banned?", predicate)
                    if ans == 'yes':
                        await ctx.invoke(ctx.bot.get_command("dungeon profiletoggle`"))
                        await asyncio.sleep(1)
        except asyncio.TimeoutError:
            pass
        try:
            cog = self.bot.get_cog("Economy")
            if cog:
                if await self._get_response(ctx, q11, predicate) == 'yes':
                    amount = await self._get_response(ctx, "How many credits should be given for using the payday command?", predicate1)
                    await ctx.invoke(ctx.bot.get_command("economyset paydayamount"), creds=amount)
                    await asyncio.sleep(1)
                    ans = await self._get_response(ctx, "Would you like to change the cooldown time for the payday command?", predicate)
                    if ans == 'yes':
                        await asyncio.sleep(1)
                        time = int(await self._get_response(ctx, "How many seconds would you like the cooldown to be?", predicate1))
                        await ctx.invoke(ctx.bot.get_command("economyset paydaytime"), seconds=time)
                        await asyncio.sleep(1)
                        register = await self._get_response(ctx, "Would you like to change the amount of credits new accounts start with?", predicate)
                        if register == 'yes':
                            await asyncio.sleep(1)
                            amount1 = await self._get_response(ctx, "How many credits would you like new accounts to start with?", predicate1)
                            await ctx.invoke(ctx.bot.get_command("economyset registeramount"), creds=amount1)
                            await asyncio.sleep(1)
        except asyncio.TimeoutError:
            pass
        try:
            cog = self.bot.get_cog("Filter")
            if cog:
                if await self._get_response(ctx, q12, predicate) == 'yes':
                    filt = await self._get_response(ctx, "What words would you like to be added to the filter? (seperate each word with a space, if it is a sentence or phrase put it insidel ""quotes"")", predicate2)
                    await ctx.invoke(ctx.bot.get_command("filter add"), words=filt)
                    await asyncio.sleep(1)
        except asyncio.TimeoutError:
            pass
        try:
            cog = self.bot.get_cog("InfoChannel")
            if cog:
                if await self._get_response(ctx, q13, predicate) == 'yes':
                    await ctx.invoke(ctx.bot.get_command("infochannel"))
                    await asyncio.sleep(1)
        except asyncio.TimeoutError:
            pass
        try:
            cog = self.bot.get_cog("Leaver")
            if cog:
                if await self._get_response(ctx, q14, predicate) == 'yes':
                    await ctx.send("**Use `]leaverset channel` in the channel you wish to recieve the messages**")
                    await asyncio.sleep(1)
        except asyncio.TimeoutError:
            pass
        try:
            cog = self.bot.get_cog("Lyrics")
            if cog:
                if await self._get_response(ctx, q15, predicate) == 'yes':
                    await asyncio.sleep(1)
                    channelmessage = await self._get_response(ctx, "What channel would you like the lyrics to go to?", predicate2)
                    channel = await (TextChannelConverter()).convert(ctx, channelmessage)
                    await ctx.invoke(ctx.bot.get_command("lyricset channel"), channel_name=channel)
                    await asyncio.sleep(1)
        except asyncio.TimeoutError:
            pass
        try:
            cog = self.bot.get_cog("Mod")
            if cog:
                if await self._get_response(ctx, q16, predicate) == 'yes':
                    repeats = await self._get_response(ctx, "Would you like to automatically delete repeated messages?", predicate)
                    if repeats == 'yes':
                        await asyncio.sleep(1)
                        await ctx.invoke(ctx.bot.get_command("modset deleterepeats"))
                        await asyncio.sleep(1)
                        delay = await self._get_response(ctx, "Would you like to automatically delete command messages?", predicate)
                        if delay == 'yes':
                            await asyncio.sleep(1)
                            delay1 = await self._get_response(ctx, "How many seconds should I wait before deleting them?", predicate1)
                            await ctx.invoke(ctx.bot.get_command("modset deletedelay"), time=delay1)
                            await asyncio.sleep(1)
        except asyncio.TimeoutError:
            pass
        try:
            cog = self.bot.get_cog("ModLog")
            if cog:
                if await self._get_response(ctx, q17, predicate) == 'yes':
                    await asyncio.sleep(1)
                    channelmessage = await self._get_response(ctx, "What channel would you like the logs to go to?", predicate2)
                    channel = await (TextChannelConverter()).convert(ctx, channelmessage)
                    await ctx.invoke(ctx.bot.get_command("modlogset modlog"), channel=channel)
                    await asyncio.sleep(1)
        except asyncio.TimeoutError:
            pass
        try:
            cog = self.bot.get_cog("Reports")
            if cog:
                if await self._get_response(ctx, q18, predicate) == 'yes':
                    await asyncio.sleep(1)
                    channelmessage = await self._get_response(ctx, "What channel would you like the reports to go to?", predicate2)
                    channel = await (TextChannelConverter()).convert(ctx, channelmessage)
                    await ctx.invoke(ctx.bot.get_command("reportset toggle"))
                    await asyncio.sleep(0.5)
                    await ctx.invoke(ctx.bot.get_command("reportset output"), channel=channel)
                    await asyncio.sleep(1)
        except asyncio.TimeoutError:
            pass
        try:
            cog = self.bot.get_cog("Starboard")
            if cog:
                if await self._get_response(ctx, q19, predicate) == 'yes':
                    await asyncio.sleep(1)
                    name = await self._get_response(ctx, "What would you like the starboard to be called?", predicate2)
                    await asyncio.sleep(0.5)
                    channelmessage = await self._get_response(ctx, "What channel would you like the starboard to be in?", predicate2)
                    channel = await (TextChannelConverter()).convert(ctx, channelmessage)
                    await ctx.invoke(ctx.bot.get_command("starboard create"), name=name, channel=channel)
                    await asyncio.sleep(1)
        except asyncio.TimeoutError:
            pass
        try:
            cog = self.bot.get_cog("Tickets")
            if cog:
                if await self._get_response(ctx, q20, predicate) == 'yes':
                    await ctx.invoke(ctx.bot.get_command("ticket set setup"))
                    await asyncio.sleep(1)
        except asyncio.TimeoutError:
            pass
        try:
            cog = self.bot.get_cog("Welcome")
            if cog:
                if await self._get_response(ctx, q21, predicate) == 'yes':
                    await ctx.invoke(ctx.bot.get_command("welcomeset leave toggle"))
                    await ctx.invoke(ctx.bot.get_command("welcomeset ban toggle"))
                    await ctx.invoke(ctx.bot.get_command("welcomeset unban toggle"))
                    await ctx.invoke(ctx.bot.get_command("welcomeset toggle"))
                    await ctx.send("Now do [p]welcomeset join msg add")
                    await ctx.send("**After you have added the new message do the following command and then type the number of the old default message**\n"
                    "`]welcomeset join msg del`")
                    await asyncio.sleep(1)
        except asyncio.TimeoutError:
            pass
        try:
            cog = self.bot.get_cog("Core")
            if cog:
                if await self._get_response(ctx, q22, predicate) == 'yes':
                    await asyncio.sleep(1)
                    rolemessage = await self._get_response(ctx, "What role would you like mods to have?", predicate2)
                    role = await commands.RoleConverter().convert(ctx, rolemessage)
                    await ctx.invoke(ctx.bot.get_command("set addmodrole"), role=role)
                    await asyncio.sleep(1)
                    role1 = await self._get_response(ctx, "What role would you like admins to have?", predicate2)
                    await ctx.invoke(ctx.bot.get_command("set addadminrole"), role=role1)
                    await asyncio.sleep(1)
        except asyncio.TimeoutError:
            pass
        try:
            cog = self.bot.get_cog("ReactRoles")
            if cog:
                if await self._get_response(ctx, q23, predicate) == 'yes':
                    await ctx.send("Use `]reactroles add ` with the message ID, channel, emoji and role.\n"
                    "**Hint: To get the message ID, turn on developer mode in Discord's appearance settings and then right click the message and click copy ID **")
        except asyncio.TimeoutError:
            return

    async def _get_response(self, ctx, question, predicate):
        question = await ctx.send(question)
        resp = await ctx.bot.wait_for('message', timeout=60, check=predicate)
        await asyncio.sleep(1)
        await resp.delete()
        await question.delete()
        return resp.content
