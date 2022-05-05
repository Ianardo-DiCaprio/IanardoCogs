import collections
import operator
import random
import time
import asyncio
from queue import Queue

import discord
from redbot.core import commands, Config
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from redbot.core.utils.chat_formatting import pagify, box


class SixMans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = PlayerQueue()
        self.game = None
        self.busy = False
        self.config = Config.get_conf(
            self, identifier=346832465834, force_registration=True
        )

        default_guild = {
            "team_size": 6,
            "latest_game_number": 0,
            "orange_team_channel": 685298673135124519,
            "blue_team_channel": 685298672333881372,
        }

        default_user = {
            "wins": 0,
            "losses": 0,
            "winloss": 0,
        }
        self.config.init_custom("GAMES", 2)
        self.config.register_custom("GAMES", blue=None, orange=None)

        self.config.register_user(**default_user)
        self.config.register_guild(**default_guild)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def smset(self, ctx, players=6):
        """Command to set between 2, 4 or 6 man"""
        if players == 2:
            await self.config.guild(ctx.guild).team_size.set(players)
            await ctx.send("6mans has been set to 2 players")
        if players == 4:
            await self.config.guild(ctx.guild).team_size.set(players)
            await ctx.send("6mans has been set to 4 players")
        if players == 6:
            await self.config.guild(ctx.guild).team_size.set(players)
            await ctx.send("6mans has been set to 6 players")

    @commands.command(pass_context=True, aliases=["q"])
    async def smqueue(self, ctx):
        """Command to join the queue"""
        player = ctx.message.author
        team_size = await self.config.guild(ctx.guild).team_size()

        if player in self.queue:
            alreadyq = "**{}** is already in the queue.".format(
                player.display_name
            )
            embed = discord.Embed(description=alreadyq, color=0x00FFFF)
            embed.set_author(
                name="PEAK LEVEL ESPORTS™ 6Mans",
                icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
            )
            await ctx.send(embed=embed)
            return
        if self.busy and player in self.game:
            alreadyg = "**{}** is already in a game.".format(
                player.display_name
            )
            embed = discord.Embed(escription=alreadyg, color=0x00FFFF)
            embed.set_author(
                name="PEAK LEVEL ESPORTS™ 6Mans",
                icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
            )
            await ctx.send(embed=embed)
            return

        if ctx.author.voice is None:
            novc = "{}: Please join a VC to join the queue.".format(
                ctx.author.mention
            )
            embed = discord.Embed(description=novc, color=0x00FFFF)
            embed.set_author(
                name="PEAK LEVEL ESPORTS™ 6Mans",
                icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
            )
            await ctx.send(embed=embed)
            return
        else:
            self.queue.put(player)
            added = "**{}** added to queue. **({}/{})**".format(
                player.display_name, self.queue.qsize(), team_size
            )
            embed = discord.Embed(description=added, color=0x00FFFF)
            embed.set_author(
                name="PEAK LEVEL ESPORTS 6Mans",
                icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
            )
            await ctx.send(embed=embed)
            if await self.queue_full(ctx):
                queuefull = "Queue is now full! Type `[v` for voting, `[c` for random captains or `[r` for random teams."
                embed = discord.Embed(description=queuefull, color=0x00FFFF)
                embed.set_author(
                    name="PEAK LEVEL ESPORTS 6Mans",
                    icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
                )
                await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=["dq"])
    async def dequeue(self, ctx):
        """Command to leave the queue"""
        player = ctx.message.author
        team_size = await self.config.guild(ctx.guild).team_size()

        if player in self.queue:
            self.queue.remove(player)
            removed = "**{}** removed from queue. **({}/{})**".format(
                player.display_name, self.queue.qsize(), team_size
            )
            embed = discord.Embed(description=removed, color=0x00FFFF)
            embed.set_author(
                name="PEAK LEVEL ESPORTS 6Mans",
                icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
            )
            await ctx.send(embed=embed)
        else:
            notq = "**{}** is not in queue.".format(player.display_name)
            embed = discord.Embed(description=notq, color=0x00FFFF)
            embed.set_author(
                name="PEAK LEVEL ESPORTS 6Mans",
                icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
            )
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def smkick(self, ctx, player: discord.Member):
        """Command to kick someone from the queue"""
        team_size = await self.config.guild(ctx.guild).team_size()
        if player in self.queue:
            self.queue.remove(player)
            kicked = "**{}** removed from queue. **({}/{})**".format(
                player.display_name, self.queue.qsize(), team_size
            )
            embed = discord.Embed(description=kicked, color=0x00FFFF)
            embed.set_author(
                name="PEAK LEVEL ESPORTS 6Mans",
                icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
            )
            await ctx.send(embed=embed)
        else:
            notq = "**{}** is not in queue.".format(player.display_name)
            embed = discord.Embed(description=notq, color=0x00FFFF)
            embed.set_author(
                name="PEAK LEVEL ESPORTS 6Mans",
                icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
            )
            await ctx.send(embed=embed)

    async def queue_full(self, ctx):
        team_size = await self.config.guild(ctx.guild).team_size()
        return self.queue.qsize() >= team_size

    def check_vote_command(self, message):
        if not message.content.startswith("[vote"):
            return False
        if not len(message.mentions) == 1:
            return False
        return True

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def smclear(self, ctx):
        """Command to clear the queue"""
        while not self.queue.empty():
            self.queue.get()
        cleared = "**{}** cleared the queue.".format(ctx.author.display_name)
        embed = discord.Embed(description=cleared, color=0x00FFFF)
        embed.set_author(
            name="PEAK LEVEL ESPORTS 6Mans",
            icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["v"])
    async def voting(self, ctx):
        """Command to start a game by voting for captains"""
        team_size = await self.config.guild(ctx.guild).team_size()
        if team_size != 6:
            await ctx.send("Voting is only allowed for 6 players.")
            return
        if not await self.queue_full(ctx):
            queuefull = "Queue is not full."
            embed = discord.Embed(description=queuefull, color=0x00FFFF)
            embed.set_author(
                name="PEAK LEVEL ESPORTS 6Mans",
                icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
            )
            await ctx.send(embed=embed)
            return
        if self.busy:
            botbusy = "Bot is busy. Please wait until picking is done."
            embed = discord.Embed(description=botbusy, color=0x00FFFF)
            embed.set_author(
                name="PEAK LEVEL ESPORTS 6Mans",
                icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
            )
            await ctx.send(embed=embed)
            return
        self.busy = True
        await self.create_game(ctx)

        captainvote = "Captain voting initiated. Use `[vote @user` to vote for a captain (cannot be yourself)."
        embed = discord.Embed(description=captainvote, color=0x00FFFF)
        embed.set_author(
            name="PEAK LEVEL ESPORTS 6Mans",
            icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
        )
        await ctx.send(embed=embed)
        available = "Available: **{}**".format(
            ", ".join([player.display_name for player in self.game.players])
        )
        embed = discord.Embed(description=available, color=0x00FFFF)
        embed.set_author(
            name="PEAK LEVEL ESPORTS 6Mans",
            icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
        )
        await ctx.send(embed=embed)
        await ctx.send("{}".format(
            ", ".join([player.mention for player in self.game.players])))

        try:
            votes = {}
            timeout = 90
            end_time = time.time() + timeout
            while len(votes) < team_size and time.time() < end_time:
                msg = await ctx.bot.wait_for(
                    "message", timeout=60, check=self.check_vote_command
                )
                if not msg:
                    continue
                if msg.author not in self.game.players:
                    return

                vote = msg.mentions[0]
                if vote == msg.author:
                    selfvote = "Cannot vote for yourself."
                    embed = discord.Embed(description=selfvote, color=0x00FFFF)
                    embed.set_author(
                        name="PEAK LEVEL ESPORTS 6Mans",
                        icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
                    )
                    await ctx.send(embed=embed)
                elif vote in self.game.players:
                    votes[msg.author] = msg.mentions[0]
                    voted = "Vote added for **{}.**".format(vote.display_name)
                    embed = discord.Embed(description=voted, color=0x00FFFF)
                    embed.set_author(
                        name="PEAK LEVEL ESPORTS 6Mans",
                        icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
                    )
                    await ctx.send(embed=embed)
                else:
                    notavailable = "**{}** not available to pick.".format(
                        vote.display_name
                    )
                    embed = discord.Embed(
                        description=notavailable, color=0x00FFFF
                    )
                    embed.set_author(
                        name="PEAK LEVEL ESPORTS 6Mans",
                        icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
                    )
                    await ctx.send(embed=embed)
        except:
            timed = "Timed out."
            embed = discord.Embed(
                title="6Mans", description=timed, color=0x00FFFF
            )
            await ctx.send(embed=embed)
        if len(votes) < team_size:
            msg = ""
            for player in self.game.players:
                if player not in votes:
                    vote = player
                    while vote == player:
                        vote = random.choice(tuple(self.game.players))
                    votes[player] = vote
                    msg += "Random vote added for **{}** from **{}**.\n".format(
                        vote.display_name, player.display_name
                    )
            embed = discord.Embed(description=msg, color=0x00FFFF)
            embed.set_author(
                name="PEAK LEVEL ESPORTS 6Mans",
                icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
            )
            await ctx.send(embed=embed)

        vote_nums = {}
        for vote in votes.values():
            vote_nums[vote] = vote_nums.get(vote, 0) + 1
        sorted_vote_nums = sorted(
            vote_nums.items(), key=operator.itemgetter(1), reverse=True
        )
        top_votes = [
            key
            for key, value in sorted_vote_nums
            if value == sorted_vote_nums[0][1]
        ]
        if len(top_votes) < 2:
            self.game.captains = top_votes
            secondary_votes = [
                key
                for key, value in sorted_vote_nums
                if value == sorted_vote_nums[1][1]
            ]
            if len(secondary_votes) > 1:
                tied = "{}-way tie for 2nd captain. Shuffling picks...".format(
                    len(secondary_votes)
                )
                embed = discord.Embed(description=tied, color=0x00FFFF)
                embed.set_author(
                    name="PEAK LEVEL ESPORTS 6Mans",
                    icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
                )
                await ctx.send(embed=embed)
                random.shuffle(secondary_votes)
            self.game.captains.append(secondary_votes[0])
        else:
            if len(top_votes) > 2:
                tieda = "{}-way tie for captains. Shuffling picks...".format(
                    len(top_votes)
                )
                embed = discord.Embed(description=tieda, color=0x00FFFF)
                embed.set_author(
                    name="PEAK LEVEL ESPORTS 6Mans",
                    icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
                )
                await ctx.send(embed=embed)
            random.shuffle(top_votes)
            self.game.captains = top_votes[:2]

        await self.do_picks(ctx)
        await self.make_channel(ctx)

        self.busy = False

    def check_orange_first_pick_command(self, message):
        if message.author != self.game.captains[0]:
            return False
        if not message.content.startswith("[pick"):
            return False
        if not len(message.mentions) == 1:
            return False
        return True

    def check_blue_picks_command(self, message):
        if message.author != self.game.captains[1]:
            return False
        if not message.content.startswith("[pick"):
            return False
        if not len(message.mentions) == 2:
            return False
        return True

    @commands.command(aliases=["c"])
    async def captains(self, ctx):
        """Command to start a game by randomly chosen captains"""
        team_size = await self.config.guild(ctx.guild).team_size()
        if team_size != 6:
            sixplayers = "Captains can only be chosen for 6 players."
            embed = discord.Embed(description=sixplayers, color=0x00FFFF)
            embed.set_author(
                name="PEAK LEVEL ESPORTS 6Mans",
                icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
            )
            await ctx.send(embed=embed)
            return
        if not self.queue_full(ctx):
            notfull = "Queue is not full."
            embed = discord.Embed(description=notfull, color=0x00FFFF)
            embed.set_author(
                name="PEAK LEVEL ESPORTS 6Mans",
                icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
            )
            await ctx.send(embed=embed)
            return
        if self.busy:
            botbusy = "Bot is busy. Please wait until picking is done."
            embed = discord.Embed(description=botbusy, color=0x00FFFF)
            embed.set_author(
                name="PEAK LEVEL ESPORTS 6Mans",
                icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
            )
            await ctx.send(embed=embed)
            return
        self.busy = True
        await self.create_game(ctx)

        await self.do_picks(ctx)

        self.busy = False

    async def do_picks(self, ctx):
        team_size = await self.config.guild(ctx.guild).team_size()
        captainchose = "Captains: {} and {}".format(
            *[captain.display_name for captain in self.game.captains]
        )
        embed = discord.Embed(description=captainchose, color=0x00FFFF)
        embed.set_author(
            name="PEAK LEVEL ESPORTS 6Mans",
            icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
        )
        await ctx.send(embed=embed)
        orange_captain = self.game.captains[0]
        self.game.add_to_orange(orange_captain)
        blue_captain = self.game.captains[1]
        self.game.add_to_blue(blue_captain)

        # Orange Pick
        await ctx.send(orange_captain.mention)
        first = "{mention} Use `[pick @user` to pick 1 player.".format(
            mention=orange_captain.display_name
        )
        embed = discord.Embed(description=first, color=0x00FFFF)
        embed.set_author(
            name="PEAK LEVEL ESPORTS 6Mans",
            icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
        )
        await ctx.send(embed=embed)
        available = "Available: {}".format(
            ", ".join([player.display_name for player in self.game.players])
        )
        embed = discord.Embed(description=available, color=0x00FFFF)
        embed.set_author(
            name="PEAK LEVEL ESPORTS 6Mans",
            icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
        )
        await ctx.send(embed=embed)
        orange_pick = None
        while not orange_pick:
            orange_pick = await self.pick_orange(ctx, orange_captain)
        self.game.add_to_orange(orange_pick)

        # Blue Picks
        await ctx.send(blue_captain.mention)
        secpick = "{mention} Use `[pick @user1 @user2` to pick 2 players.".format(
            mention=blue_captain.display_name
        )
        embed = discord.Embed(description=secpick, color=0x00FFFF)
        embed.set_author(
            name="PEAK LEVEL ESPORTS 6Mans",
            icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
        )
        await ctx.send(embed=embed)
        availabletwo = "Available: {}".format(
            ", ".join([player.display_name for player in self.game.players])
        )
        embed = discord.Embed(description=availabletwo, color=0x00FFFF)
        embed.set_author(
            name="PEAK LEVEL ESPORTS 6Mans",
            icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
        )
        await ctx.send(embed=embed)
        blue_picks = None
        while not blue_picks:
            blue_picks = await self.pick_blue(ctx, blue_captain)
        for blue_pick in blue_picks:
            self.game.add_to_blue(blue_pick)

        # Orange Player
        last_player = next(iter(self.game.players))
        self.game.add_to_orange(last_player)
        oradded = "{} added to 🔶 ORANGE 🔶 team.".format(
            last_player.display_name
        )
        embed = discord.Embed(description=oradded, color=0x00FFFF)
        embed.set_author(
            name="PEAK LEVEL ESPORTS 6Mans",
            icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
        )
        await ctx.send(embed=embed)
        await self.display_teams(ctx)
        await self.make_channel(ctx)

    async def pick_orange(self, ctx, captain):
        try:
            msg = await ctx.bot.wait_for(
                "message",
                timeout=60,
                check=self.check_orange_first_pick_command,
            )
            if msg:
                pick = msg.mentions[0]
                if pick not in self.game.players:
                    notav = "{} not available to pick.".format(
                        pick.display_name
                    )
                    embed = discord.Embed(description=notav, color=0x00FFFF)
                    embed.set_author(
                        name="VPEAK LEVEL ESPORTS 6Mans",
                        icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
                    )
                    await ctx.send(embed=embed)
                    return None
                orpick = "Picked {} for 🔶 ORANGE 🔶 team.".format(
                    pick.display_name
                )
                embed = discord.Embed(description=orpick, color=0x00FFFF)
                embed.set_author(
                    name="PEAK LEVEL ESPORTS 6Mans",
                    icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
                )
                await ctx.send(embed=embed)
                return pick
        except:
            pick = random.choice(tuple(self.game.players))
            timedout = "Timed out. Randomly picked {} for 🔶 ORANGE 🔶 team.".format(
                pick.display_name
            )
            embed = discord.Embed(description=timedout, color=0x00FFFF)
            embed.set_author(
                name="PEAK LEVEL ESPORTS 6Mans",
                icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
            )
            await ctx.send(embed=embed)
            return pick

    async def pick_blue(self, ctx, captain):
        try:
            msg = await ctx.bot.wait_for(
                "message", timeout=60, check=self.check_blue_picks_command
            )
            if msg:
                picks = msg.mentions
                for pick in picks:
                    if pick not in self.game.players:
                        notav = "{} not available to pick.".format(
                            pick.display_name
                        )
                        embed = discord.Embed(
                            title="PEAK LEVEL ESPORTS 6Mans",
                            description=notav,
                            color=0x00FFFF,
                        )
                        embed.set_thumbnail(
                            url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png"
                        )
                        await ctx.send(embed=embed)
                        return None
                    twopick = "Picked {} and {} for 🔷 BLUE 🔷 team.".format(
                        *[pick.display_name for pick in picks]
                    )
                    embed = discord.Embed(
                        title="PEAK LEVEL ESPORTS 6Mans",
                        description=twopick,
                        color=0x00FFFF,
                    )
                    embed.set_thumbnail(
                        url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png"
                    )
                    await ctx.send(embed=embed)
                    return picks
        except:
            picks = random.sample(self.game.players, 2)
            timed = "Timed out. Randomly picked {} and {} for 🔷 BLUE 🔷 team.".format(
                *[pick.display_name for pick in picks]
            )
            embed = discord.Embed(
                title="PEAK LEVEL ESPORTS 6Mans", description=timed, color=0x00FFFF
            )
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png"
            )
            await ctx.send(embed=embed)
            return picks

    @commands.command(aliases=["r"])
    async def random(self, ctx):
        """Command to start a game by randomly assigning teams"""
        if not await self.queue_full(ctx):
            notfull = "Queue is not full."
            embed = discord.Embed(description=notfull, color=0x00FFFF)
            embed.set_author(
                name="PEAK LEVEL ESPORTS 6Mans",
                icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
            )
            await ctx.send(embed=embed)
            return
        if self.busy:
            busy = "Bot is busy. Please wait until picking is done."
            embed = discord.Embed(description=busy, color=0x00FFFF)
            embed.set_author(
                name="PEAK LEVEL ESPORTS 6Mans",
                icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
            )
            await ctx.send(embed=embed)
            return
        self.busy = True
        await self.create_game(ctx)
        team_size = await self.config.guild(ctx.guild).team_size()
        sizes = round(team_size / 2)
        orange = random.sample(self.game.players, sizes)
        for player in orange:
            self.game.add_to_orange(player)

        blue = list(self.game.players)
        for player in blue:
            self.game.add_to_blue(player)

        await self.display_teams(ctx)
        await self.make_channel(ctx)

        self.busy = False

    async def display_teams(self, ctx):
        embed = discord.Embed(title="PEAK LEVEL ESPORTS 6Mans", color=0x00FFFF)
        blue = "🔷 BLUE 🔷: **{}**".format(
            ", ".join([player.display_name for player in self.game.blue])
        )
        orange = "🔶 ORANGE 🔶: **{}**".format(
            ", ".join([player.display_name for player in self.game.orange])
        )
        next_game_number = (
            await self.config.guild(ctx.guild).latest_game_number() + 1
        )
        embed.add_field(name="**Blue Team:**", value=blue, inline=False)
        embed.add_field(name="**Orange Team:**", value=orange, inline=False)
        embed.add_field(
            name="**Game Code:**", value=next_game_number, inline=False
        )
        embed.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png"
        )
        await ctx.send(embed=embed)
        await ctx.send("{}".format(
            ", ".join([player.mention for player in self.game.blue])))
        await ctx.send("{}".format(
            ", ".join([player.mention for player in self.game.orange])))

        async with self.config.guild(ctx.guild).latest_game_number.get_lock():
            next_game_number = (
                await self.config.guild(ctx.guild).latest_game_number() + 1
            )
            await self.config.custom(
                "GAMES", ctx.guild.id, next_game_number
            ).blue.set([player.id for player in self.game.blue])
            await self.config.custom(
                "GAMES", ctx.guild.id, next_game_number
            ).orange.set([player.id for player in self.game.orange])
            await self.config.guild(ctx.guild).latest_game_number.set(
                next_game_number
            )

    async def create_game(self, ctx):
        team_size = await self.config.guild(ctx.guild).team_size()
        players = [self.queue.get() for _ in range(team_size)]
        self.game = Game(players)

    async def make_channel(self, ctx):
        orangeteam = (player.id for player in self.game.orange)
        blueteam = (player.id for player in self.game.blue)
        orangechannel = await self.config.guild(
            ctx.guild
        ).orange_team_channel()
        bluechannel = await self.config.guild(ctx.guild).blue_team_channel()
        createdblue = ctx.bot.get_channel(bluechannel)
        createdorange = ctx.bot.get_channel(orangechannel)
        for player in blueteam:
            member = ctx.guild.get_member(player)
            current_voice = member.voice.channel if member.voice else None
            if current_voice and ctx.guild.me.guild_permissions.move_members:
                await member.move_to(createdblue)
        for player in orangeteam:
            member = ctx.guild.get_member(player)
            current_voice = member.voice.channel if member.voice else None
            if current_voice and ctx.guild.me.guild_permissions.move_members:
                await member.move_to(createdorange)

    @commands.command(aliases=["smr"])
    async def smreport(self, ctx, code: int, team):
        """Command to report game results."""
        if not str(code).isnumeric():
            await ctx.send("Please use the correct code.")
            return
        if team:
             team = team.capitalize()
        if team != "Blue":
            if team != "Orange":
                await ctx.send("Please use `Blue` or `Orange` for the team.")
        orange = await self.config.custom("GAMES", ctx.guild.id, code).orange()
        blue = await self.config.custom("GAMES", ctx.guild.id, code).blue()
        if not blue:
            await ctx.send("This game has already been reported or the code doesn't exist.")
            return
        if not orange:
            await ctx.send("This game has already been reported or the code doesn't exist.")
            return
        if ctx.author.id in orange or blue:
            if team == "Orange":
                for users in orange:
                    user = ctx.guild.get_member(users)
                    wins = await self.config.user(user).wins()
                    losses = await self.config.user(user).losses()
                    new_win = wins + 1
                    if losses == 0:
                        winloss = 100
                    else:
                        new = losses + new_win
                        winloss = round(new_win / new * 100, 2)
                    await self.config.user(user).wins.set(new_win)
                    await self.config.user(user).winloss.set(winloss)
                    report = "**{}** now has **{wins} win/s**. **{losses} loss/es** and a win/loss of **{winloss}%**".format(
                        user.mention,
                        wins=new_win,
                        losses=losses,
                        winloss=winloss,
                    )
                    embed = discord.Embed(description=report, color=0x00FFFF)
                    embed.set_author(
                        name="PEAK LEVEL ESPORTS 6Mans",
                        icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
                    )
                    await ctx.send(embed=embed)
                for users in blue:
                    user = ctx.guild.get_member(users)
                    wins = await self.config.user(user).wins()
                    losses = await self.config.user(user).losses()
                    new_loss = losses + 1
                    new = wins + new_loss
                    winloss = round(wins / new * 100, 2)
                    await self.config.user(user).losses.set(new_loss)
                    await self.config.user(user).winloss.set(winloss)
                    report = "**{}** now has **{wins} win/s**. **{losses} loss/es** and a win/loss of **{winloss}%**".format(
                        user.mention,
                        wins=wins,
                        losses=new_loss,
                        winloss=winloss,
                    )
                    embed = discord.Embed(description=report, color=0x00FFFF)
                    embed.set_author(
                        name="PEAK LEVEL ESPORTS 6Mans",
                        icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
                    )
                    await ctx.send(embed=embed)
        
            if team == "Blue":
                for users in blue:
                    user = ctx.guild.get_member(users)
                    wins = await self.config.user(user).wins()
                    losses = await self.config.user(user).losses()
                    new_win = wins + 1
                    if losses == 0:
                        winloss = 100
                    else:
                        new = losses + new_win
                        winloss = round(new_win / new * 100, 2)
                    await self.config.user(user).wins.set(new_win)
                    await self.config.user(user).winloss.set(winloss)
                    report = "**{}** now has **{wins} win/s**. **{losses} loss/es** and a win/loss of **{winloss}%**".format(
                        user.mention,
                        wins=new_win,
                        losses=losses,
                        winloss=winloss,
                    )
                    embed = discord.Embed(description=report, color=0x00FFFF)
                    embed.set_author(
                        name="PEAK LEVEL ESPORTS 6Mans",
                        icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
                    )
                    await ctx.send(embed=embed)
                for users in orange:
                    user = ctx.guild.get_member(users)
                    wins = await self.config.user(user).wins()
                    losses = await self.config.user(user).losses()
                    new_loss = losses + 1
                    new = wins + new_loss
                    winloss = round(wins / new * 100, 2)
                    await self.config.user(user).losses.set(new_loss)
                    await self.config.user(user).winloss.set(winloss)
                    report = "**{}** now has **{wins} win/s**. **{losses} loss/es** and a win/loss of **{winloss}%**".format(
                        user.mention,
                        wins=wins,
                        losses=new_loss,
                        winloss=winloss,
                    )
                    embed = discord.Embed(description=report, color=0x00FFFF)
                    embed.set_author(
                        name="PEAK LEVEL ESPORTS 6Mans",
                        icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
                    )
                    await ctx.send(embed=embed)
        else:
            await ctx.send("You were not in this game so you cannot report it")

        await self.config.custom("GAMES", ctx.guild.id, code).orange.clear()
        await self.config.custom("GAMES", ctx.guild.id, code).blue.clear()

    @commands.command()
    async def smtop(self, ctx):
        """Command to show the 6Mans leaderboard."""
        embeds = []
        msg = ""
        users = await self.config.all_users()
        test = sorted(users, key=lambda a: (users[a]["wins"], users[a]["winloss"]), reverse=True)
        for user in test:
            wins = users[user]["wins"]
            losses = users[user]["losses"]
            winloss = users[user]["winloss"]
            try:
                user = ctx.guild.get_member(user)
                msg += (
                    f"{user.display_name}".ljust(11, " ")[:11]
                    + (f":".ljust(3, " "))
                    + (f" Wins: {wins}".ljust(13, " "))
                    + (f"Losses: {losses}".ljust(13, " "))
                    + f"Win/Loss: {winloss}%\n"
                )
            except:
                return
        for msg in pagify(msg):
            embed = discord.Embed(color=0x00FFFF)
            embed.description = box(msg)
            embed.set_author(
                name="PEAK LEVEL ESPORTS 6Mans Leaderboard",
                icon_url="https://cdn.discordapp.com/attachments/766330956680003615/963188931791319070/croppedCarbon.png",
            )
            embeds.append(embed)
        await menu(ctx, embeds, DEFAULT_CONTROLS)


class Game:
    def __init__(self, players):
        self.players = set(players)
        self.captains = random.sample(self.players, 2)
        self.orange = set()
        self.blue = set()

    def add_to_blue(self, player):
        self.players.remove(player)
        self.blue.add(player)

    def add_to_orange(self, player):
        self.players.remove(player)
        self.orange.add(player)

    def __contains__(self, item):
        return item in self.players or item in self.orange or item in self.blue


class OrderedSet(collections.MutableSet):
    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]  # sentinel node for doubly linked list
        self.map = {}  # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            key, prev, next = self.map.pop(key)
            prev[2] = next
            next[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if not self:
            raise KeyError("set is empty")
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return "%s()" % (self.__class__.__name__,)
        return "%s(%r)" % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)


class PlayerQueue(Queue):
    def _init(self, maxsize):
        self.queue = OrderedSet()

    def _put(self, item):
        self.queue.add(item)

    def _get(self):
        return self.queue.pop()

    def remove(self, value):
        self.queue.remove(value)

    def __contains__(self, item):
        with self.mutex:
            return item in self.queue
