import discord
from redbot.core import commands, Config
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from redbot.core.utils.chat_formatting import pagify

class GamerTag(commands.Cog):
    """GamerTag cog"""

    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, identifier=699114201327)

        default_user = {
            "playlstationgamertag": None,
            "xboxgamertag": None,
            "epicgamesgamertag": None,
            "battlenetgamertag": None,
            "uplaygamertag": None,
            "steamgamertag": None,
            "nintendogamertag": None,
        }

        self.conf.register_user(**default_user)

    @commands.command()
    async def psnset(self, ctx, gamertag=None):
        """Command to set your playstation gamertag"""
        if gamertag:
            await self.conf.user(ctx.author).playstationgamertag.set(gamertag)
            await ctx.send("Your playstation gamertag has been set.")
        else:
            await self.conf.user(ctx.author).playstationgamertag.set(gamertag)
            await ctx.send("Your playstation gamertag has been removed.")

    @commands.command()
    async def xbset(self, ctx, gamertag=None):
        """Command to set your Xbox gamertag"""
        if gamertag:
            await self.conf.user(ctx.author).xboxgamertag.set(gamertag)
            await ctx.send("Your Xbox gamertag has been set.")
        else:
            await self.conf.user(ctx.author).xboxgamertag.set(gamertag)
            await ctx.send("Your Xbox gamertag has been removed.")

    @commands.command()
    async def epicset(self, ctx, gamertag=None):
        """Command to set your Epic Games gamertag"""
        if gamertag:
            await self.conf.user(ctx.author).epicgamesgamertag.set(gamertag)
            await ctx.send("Your Epic Games gamertag has been set.")
        else:
            await self.conf.user(ctx.author).epicgamesgamertag.set(gamertag)
            await ctx.send("Your Epic Games gamertag has been removed.")

    @commands.command()
    async def bnset(self, ctx, gamertag=None):
        """Command to set your Battle.net gamertag"""
        if gamertag:
            await self.conf.user(ctx.author).battlenetgamertag.set(gamertag)
            await ctx.send("Your Battle.net gamertag has been set.")
        else:
            await self.conf.user(ctx.author).battlenetgamertag.set(gamertag)
            await ctx.send("Your Battle.net gamertag has been removed.")

    @commands.command()
    async def uplayset(self, ctx, gamertag=None):
        """Command to set your Uplay gamertag"""
        if gamertag:
            await self.conf.user(ctx.author).uplaygamertag.set(gamertag)
            await ctx.send("Your Uplay gamertag has been set.")
        else:
            await self.conf.user(ctx.author).uplaygamertag.set(gamertag)
            await ctx.send("Your Uplay gamertag has been removed.")

    @commands.command()
    async def steamset(self, ctx, gamertag=None):
        """Command to set your Steam gamertag"""
        if gamertag:
            await self.conf.user(ctx.author).steamgamertag.set(gamertag)
            await ctx.send("Your Steam gamertag has been set.")
        else:
            await self.conf.user(ctx.author).steamgamertag.set(gamertag)
            await ctx.send("Your Steam gamertag has been removed.")

    @commands.command()
    async def ndset(self, ctx, gamertag=None):
        """Command to set your Nintendo gamertag"""
        if gamertag:
            await self.conf.user(ctx.author).nintendogamertag.set(gamertag)
            await ctx.send("Your Nintendo gamertag has been set.")
        else:
            await self.conf.user(ctx.author).nintendogamertag.set(gamertag)
            await ctx.send("Your Nintendo gamertag has been removed.")

    @commands.command(aliases=["psn"])
    async def psngamertag(self, ctx, user: discord.Member = None):
        """Command to get a users Playstation gamertag if no user is given it will get yours."""
        if user is None:
            user = ctx.author
        psgamertag = await self.conf.user(user).playstationgamertag()
        if psgamertag:
            await ctx.send(f"This user's Playstation gamertag is: {psgamertag}")
        else:
            await ctx.send("This user hasn't set a Playstation gamertag.")

    @commands.command(aliases=["xbox"])
    async def xbgamertag(self, ctx, user: discord.Member = None):
        """Command to get a users Xbox gamertag if no user is given it will get yours."""
        if user is None:
            user = ctx.author
        xbgamertag = await self.conf.user(user).xboxgamertag()
        if xbgamertag:
            await ctx.send(f"This user's Xbox gamertag is: {xbgamertag}")
        else:
            await ctx.send("This user hasn't set a Xbox gamertag.")

    @commands.command(aliases=["epic"])
    async def eggamertag(self, ctx, user: discord.Member = None):
        """Command to get a users Epic Games gamertag if no user is given it will get yours."""
        if user is None:
            user = ctx.author
        eggamertag = await self.conf.user(user).epicgamesgamertag()
        if eggamertag:
            await ctx.send(f"This user's Epic Games gamertag is: {eggamertag}")
        else:
            await ctx.send("This user hasn't set an Epic Games gamertag.")

    @commands.command(aliases=["bnet"])
    async def bngamertag(self, ctx, user: discord.Member = None):
        """Command to get a users Battle.net gamertag if no user is given it will get yours."""
        if user is None:
            user = ctx.author
        bngamertag = await self.conf.user(user).battlenetgamertag()
        if bngamertag:
            await ctx.send(f"This user's Battle.net gamertag is: {bngamertag}")
        else:
            await ctx.send("This user hasn't set a Battle.net gamertag.")

    @commands.command(aliases=["uplay"])
    async def upgamertag(self, ctx, user: discord.Member = None):
        """Command to get a users Uplay gamertag if no user is given it will get yours."""
        if user is None:
            user = ctx.author
        upgamertag = await self.conf.user(user).uplaygamertag()
        if upgamertag:
            await ctx.send(f"This user's Uplay gamertag is: {upgamertag}")
        else:
            await ctx.send("This user hasn't set a Uplay gamertag.")

    @commands.command(aliases=["steam"])
    async def steamgamertag(self, ctx, user: discord.Member = None):
        """Command to get a users Steam gamertag if no user is given it will get yours."""
        if user is None:
            user = ctx.author
        steamgamertag = await self.conf.user(user).nintendogamertag()
        if steamgamertag:
            await ctx.send(f"This user's Steam gamertag is: {steamgamertag}")
        else:
            await ctx.send("This user hasn't set a Steam gamertag.")

    @commands.command(aliases=["nintendo"])
    async def ndgamertag(self, ctx, user: discord.Member = None):
        """Command to get a users Nintendo gamertag if no user is given it will get yours."""
        if user is None:
            user = ctx.author
        nintendogamertag = await self.conf.user(user).nintendogamertag()
        if nintendogamertag:
            await ctx.send(f"This user's Nintendo gamertag is: {nintendogamertag}")
        else:
            await ctx.send("This user hasn't set a Nintendo gamertag.")

    @commands.command()
    async def psnlist(self, ctx):
        """Command to get a list of users Playstation gamertags"""
        embeds = []
        msg = ""
        guild = ctx.guild
        users = await self.conf.all_users()
        for user_id, gamertag in users.items():
            gamertagitems = gamertag.items()
            for k, v in gamertagitems:
                if "playstationgamertag" in k:
                    if v is not None:
                        if user_id in [x.id for x in guild.members]:
                            msg += f"<@{user_id}>'s Playstation gamertag is: {v}\n"
        if msg == "":
            msg = "**No users have set their Playstation gamertag.**"
        for msg in pagify(msg):
            embed = discord.Embed(title="Playstation gamertags", color=0x0000CC)
            embed.description = msg
            embeds.append(embed)
        await menu(ctx, embeds, DEFAULT_CONTROLS)

    @commands.command()
    async def xblist(self, ctx):
        """Command to get a list of users Xbox gamertags"""
        embeds = []
        msg = ""
        guild = ctx.guild
        users = await self.conf.all_users()
        for user_id, gamertag in users.items():
            gamertagitems = gamertag.items()
            for k, v in gamertagitems:
                if "xboxgamertag" in k:
                    if v is not None:
                        if user_id in [x.id for x in guild.members]:
                            msg += f"<@{user_id}>'s Xbox gamertag is: {v}\n"
        if msg == "":
            msg = "**No users have set their Xbox gamertag.**"
        for msg in pagify(msg):
            embed = discord.Embed(title="Xbox gamertags", color=0x00CC00)
            embed.description = msg
            embeds.append(embed)
        await menu(ctx, embeds, DEFAULT_CONTROLS)

    @commands.command()
    async def eglist(self, ctx):
        """Command to get a list of users Epic Games gamertags"""
        embeds = []
        msg = ""
        guild = ctx.guild
        users = await self.conf.all_users()
        for user_id, gamertag in users.items():
            gamertagitems = gamertag.items()
            for k, v in gamertagitems:
                if "epicgamesgamertag" in k:
                    if v is not None:
                        if user_id in [x.id for x in guild.members]:
                            msg += f"<@{user_id}>'s Epic Games gamertag is: {v}\n"
        if msg == "":
            msg = "**No users have set their Epic Games gamertag.**"
        for msg in pagify(msg):
            embed = discord.Embed(title="Epic Games gamertags", color=0x202020)
            embed.description = msg
            embeds.append(embed)
        await menu(ctx, embeds, DEFAULT_CONTROLS)

    @commands.command()
    async def bnlist(self, ctx):
        """Command to get a list of users Battle.net gamertags"""
        embeds = []
        msg = ""
        guild = ctx.guild
        users = await self.conf.all_users()
        for user_id, gamertag in users.items():
            gamertagitems = gamertag.items()
            for k, v in gamertagitems:
                if "battlenetgamertag" in k:
                    if v is not None:
                        if user_id in [x.id for x in guild.members]:
                            msg += f"<@{user_id}>'s Battle.net gamertag is: {v}\n"
        if msg == "":
            msg = "**No users have set their Battle.net gamertag.**"
        for msg in pagify(msg):
            embed = discord.Embed(title="Battle.net gamertags", color=0x000099)
            embed.description = msg
            embeds.append(embed)
        await menu(ctx, embeds, DEFAULT_CONTROLS)

    @commands.command()
    async def uplist(self, ctx):
        """Command to get a list of users Uplay gamertags"""
        embeds = []
        msg = ""
        guild = ctx.guild
        users = await self.conf.all_users()
        for user_id, gamertag in users.items():
            gamertagitems = gamertag.items()
            for k, v in gamertagitems:
                if "uplaygamertag" in k:
                    if v is not None:
                        if user_id in [x.id for x in guild.members]:
                            msg += f"<@{user_id}>'s Uplay gamertag is: {v}\n"
        if msg == "":
            msg = "**No users have set their Uplay gamertag.**"
        for msg in pagify(msg):
            embed = discord.Embed(title="Uplay gamertags", color=0x0080FF)
            embed.description = msg
            embeds.append(embed)
        await menu(ctx, embeds, DEFAULT_CONTROLS)

    @commands.command()
    async def steamlist(self, ctx):
        """Command to get a list of users Steam gamertags"""
        embeds = []
        msg = ""
        guild = ctx.guild
        users = await self.conf.all_users()
        for user_id, gamertag in users.items():
            gamertagitems = gamertag.items()
            for k, v in gamertagitems:
                if "steamgamertag" in k:
                    if v is not None:
                        if user_id in [x.id for x in guild.members]:
                            msg += f"<@{user_id}>'s Steam gamertag is: {v}\n"
        if msg == "":
            msg = "**No users have set their Steam gamertag.**"
        for msg in pagify(msg):
            embed = discord.Embed(title="Steam gamertags", color=0x404040)
            embed.description = msg
            embeds.append(embed)
        await menu(ctx, embeds, DEFAULT_CONTROLS)

    @commands.command()
    async def ndlist(self, ctx):
        """Command to get a list of users Nintendo gamertags"""
        embeds = []
        msg = ""
        guild = ctx.guild
        users = await self.conf.all_users()
        for user_id, gamertag in users.items():
            gamertagitems = gamertag.items()
            for k, v in gamertagitems:
                if "nintendogamertag" in k:
                    if v is not None:
                        if user_id in [x.id for x in guild.members]:
                            msg += f"<@{user_id}>'s Nintendo gamertag is: {v}\n"
        if msg == "":
            msg = "**No users have set their Nintendo gamertag.**"
        for msg in pagify(msg):
            embed = discord.Embed(title="Nintendo gamertags", color=0x404040)
            embed.description = msg
            embeds.append(embed)
        await menu(ctx, embeds, DEFAULT_CONTROLS)
