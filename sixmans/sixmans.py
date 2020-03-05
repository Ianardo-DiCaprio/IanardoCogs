import collections
import operator
import random
import time
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
        self.config = Config.get_conf(self, identifier=346832465834, force_registration=True)

        default_guild = {
            "team_size": 6,
            "latest_game_number": 0,
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
            alreadyq = ("**{}** is already in the queue.".format(player.display_name))
            embed = discord.Embed(title="VOID ESPORTS™ 6Mans", description=alreadyq, color=0x00FFFF)
            await ctx.send(embed=embed)
            return
        if self.busy and player in self.game:
            alreadyg = ("**{}** is already in a game.".format(player.display_name))
            embed = discord.Embed(title="VOID ESPORTS™ 6Mans", description=alreadyg, color=0x00FFFF)
            await ctx.send(embed=embed)
            return

        self.queue.put(player)

        added = ("**{}** added to queue. **({}/{})**".format(player.display_name, self.queue.qsize(), team_size))
        embed = discord.Embed(title="VOID ESPORTS™ 6Mans", description=added, color=0x00FFFF)
        await ctx.send(embed=embed)
        if await self.queue_full(ctx):
            queuefull = ("Queue is now full! Type `[v`,  `[c` or `[r` to create a game.")
            embed = discord.Embed(title="VOID ESPORTS™ 6Mans", description=queuefull, color=0x00FFFF)
            await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=["dq"])
    async def dequeue(self, ctx):
        """Command to leave the queue"""
        player = ctx.message.author
        team_size = await self.config.guild(ctx.guild).team_size()

        if player in self.queue:
            await self.queue.remove(player)
            removed = (
                "**{}** removed from queue. **({}/{})**".format(player.display_name, self.queue.qsize(), team_size))
            embed = discord.Embed(title="VOID ESPORTS™ 6Mans", description=removed, color=0x00FFFF)
            await ctx.send(embed=embed)
        else:
            notq = ("**{}** is not in queue.".format(player.display_name))
            embed = discord.Embed(title="VOID ESPORTS™ 6Mans", description=notq, color=0x00FFFF)
            await ctx.send(embed=embed)

    @commands.command()
    async def smkick(self, ctx,  player: discord.Member):
        """Command to kick someone from the queue"""
        team_size = await self.config.guild(ctx.guild).team_size()
        if player in self.queue:
            self.queue.remove(player)
            kicked = (
                "**{}** removed from queue. **({}/{})**".format(player.display_name, self.queue.qsize(), team_size))
            embed = discord.Embed(title="VOID ESPORTS™ 6Mans", description=kicked, color=0x00FFFF)
            await ctx.send(embed=embed)
        else:
            notq = ("**{}** is not in queue.".format(player.display_name))
            embed = discord.Embed(title="VOID ESPORTS™ 6Mans", description=notq, color=0x00FFFF)
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
    async def smclear(self, ctx):
        """Command to clear the queue"""
        team_size = await self.config.guild(ctx.guild).team_size()
        players = self.queue.get()
        cleared = (
            "**{}** cleared the queue.".format(ctx.author.display_name))
        embed = discord.Embed(title="VOID ESPORTS™ 6Mans", description=cleared, color=0x00FFFF)
        await ctx.send(embed=embed)

    @commands.command(aliases=["v"])
    async def voting(self, ctx):
        """Command to start a game by voting for captains"""
        team_size = await self.config.guild(ctx.guild).team_size()
        if team_size == 2:
            await ctx.send("There is only 2 players, you can't vote for captains")
            return
        if not await self.queue_full(ctx):
            queuefull = ("Queue is not full.")
            embed = discord.Embed(title="VOID ESPORTS™ 6Mans", description=queuefull, color=0x00FFFF)
            await ctx.send(embed=embed)
            return
        if self.busy:
            botbusy = ("Bot is busy. Please wait until picking is done.")
            embed = discord.Embed(title="VOID ESPORTS™ 6Mans", description=botbusy, color=0x00FFFF)
            await ctx.send(embed=embed)
            return
        self.busy = True
        await self.create_game(ctx)

        captainvote = ("Captain voting initiated. Use [vote [user] to vote for a captain (cannot be yourself).")
        embed = discord.Embed(title="VOID ESPORTS™ 6Mans", description=captainvote, color=0x00FFFF)
        await ctx.send(embed=embed)
        available = ("Available: **{}**".format(", ".join([player.display_name for player in self.game.players])))
        embed = discord.Embed(title="VOID ESPORTS™ 6Mans", description=available, color=0x00FFFF)
        await ctx.send(embed=embed)

        votes = {}
        timeout = 90
        end_time = time.time() + timeout
        while len(votes) < team_size and time.time() < end_time:
            msg = await ctx.bot.wait_for("message", timeout=60, check=self.check_vote_command)
            if not msg:
                continue
            if msg.author not in self.game.players:
                return

            vote = msg.mentions[0]
            if vote == msg.author:
                selfvote = ("Cannot vote for yourself.")
                embed = discord.Embed(title="6Mans", description=selfvote, color=0x00FFFF)
                await ctx.send(embed=embed)
            elif vote in self.game.players:
                votes[msg.author] = msg.mentions[0]
                voted = ("Vote added for **{}.**".format(vote.display_name))
                embed = discord.Embed(title="6Mans", description=voted, color=0x00FFFF)
                await ctx.send(embed=embed)
            else:
                notavailable = ("**{}** not available to pick.".format(vote.display_name))
                embed = discord.Embed(title="6Mans", description=notavailable, color=0x00FFFF)
                await ctx.send(embed=embed)
        if len(votes) < team_size:
            timed = ("Timed out.")
            embed = discord.Embed(title="6Mans", description=timed, color=0x00FFFF)
            await ctx.send(embed=embed)
            msg = ""
            for player in self.game.players:
                if player not in votes:
                    vote = player
                    while vote == player:
                        vote = random.choice(tuple(self.game.players))
                    votes[player] = vote
                    msg += "Random vote added for **{}** from **{}**.\n".format(vote.display_name, player.display_name)
            embed = discord.Embed(title="VOID ESPORTS™ 6Mans", description=msg, color=0x00FFFF)
            await ctx.send(embed=embed)

        vote_nums = {}
        for vote in votes.values():
            vote_nums[vote] = vote_nums.get(vote, 0) + 1
        sorted_vote_nums = sorted(vote_nums.items(), key=operator.itemgetter(1), reverse=True)
        top_votes = [key for key, value in sorted_vote_nums if value == sorted_vote_nums[0][1]]
        if len(top_votes) < 2:
            self.game.captains = top_votes
            secondary_votes = [key for key, value in sorted_vote_nums if value == sorted_vote_nums[1][1]]
            if len(secondary_votes) > 1:
                tied = ("{}-way tie for 2nd captain. Shuffling picks...".format(len(secondary_votes)))
                embed = discord.Embed(title="VOID ESPORTS™ 6Mans", description=tied, color=0x00FFFF)
                await ctx.send(embed=embed)
                random.shuffle(secondary_votes)
            self.game.captains.append(secondary_votes[0])
        else:
            if len(top_votes) > 2:
                tieda = ("{}-way tie for captains. Shuffling picks...".format(len(top_votes)))
                embed = discord.Embed(title="VOID ESPORTS™ 6Mans", description=tieda, color=0x00FFFF)
                await ctx.send(embed=embed)
            random.shuffle(top_votes)
            self.game.captains = top_votes[:2]

        await self.do_picks()

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
            await ctx.send("Captains can only be chosen for 6 players.")
            return
        if not self.queue_full(ctx):
            await ctx.send("Queue is not full.")
            return
        if self.busy:
            await ctx.send("Bot is busy. Please wait until picking is done.")
            return
        self.busy = True
        await self.create_game(ctx)

        await self.do_picks(ctx)

        self.busy = False

    async def do_picks(self, ctx):
        team_size = await self.config.guild(ctx.guild).team_size()
        await ctx.send("Captains: {} and {}".format(*[captain.display_name for captain in self.game.captains]))
        orange_captain = self.game.captains[0]
        self.game.add_to_orange(orange_captain)
        blue_captain = self.game.captains[1]
        self.game.add_to_blue(blue_captain)

        # Orange Pick
        await ctx.send(
            "{mention} Use [pick [user] to pick 1 player.".format(mention=orange_captain.display_name))
        await ctx.send("Available: {}".format(", ".join([player.display_name for player in self.game.players])))
        orange_pick = None
        while not orange_pick:
            orange_pick = await self.pick_orange(ctx, orange_captain)
        self.game.add_to_orange(orange_pick)

        # Blue Picks
        await ctx.send(
            "{mention} Use [pick [user1] [user2] to pick 2 players.".format(mention=blue_captain.display_name))
        await ctx.send("Available: {}".format(", ".join([player.display_name for player in self.game.players])))
        blue_picks = None
        while not blue_picks:
            blue_picks = await self.pick_blue(ctx, blue_captain)
        for blue_pick in blue_picks:
            self.game.add_to_blue(blue_pick)

        # Orange Player
        last_player = next(iter(self.game.players))
        self.game.add_to_orange(last_player)
        await ctx.say("{} added to 🔶 ORANGE 🔶 team.".format(last_player.mention))
        await self.display_teams(ctx)

    async def pick_orange(self, ctx, captain):
    try:
        msg = await ctx.bot.wait_for("message", timeout=10, check=self.check_orange_first_pick_command)
        if msg:
            pick = msg.mentions[0]
            if pick not in self.game.players:
                await ctx.send("{} not available to pick.".format(pick.display_name))
                return None
            await ctx.send("Picked {} for 🔶 ORANGE 🔶 team.".format(pick.mention))
            return pick
    except:
        pick = random.choice(tuple(self.game.players))
        await ctx.send("Timed out. Randomly picked {} for 🔶 ORANGE 🔶 team.".format(pick.mention))
        return pick


    async def pick_blue(self, ctx, blue_captain):
        try:
            msg = await self.bot.wait_for_message(timeout=90, author=captain, check=self.check_blue_picks_command)
            if msg:
                picks = msg.mentions
                for pick in picks:
                    if pick not in self.game.players:
                        await self.bot.say("{} not available to pick.".format(pick.display_name))
                        return None
                    await self.bot.say("Picked {} and {} for 🔷 BLUE 🔷 team.".format(*[pick.mention for pick in picks]))
                    return picks
        else:
            picks = random.sample(self.game.players, 2)
            await self.bot.say(
                "Timed out. Randomly picked {} and {} for 🔷 BLUE 🔷 team.".format(*[pick.mention for pick in picks]))
            return picks

    @commands.command(aliases=["r"])
    async def random(self, ctx):
        """Command to start a game by randomly assigning teams"""
        if not await self.queue_full(ctx):
            notfull = ("Queue is not full.")
            embed = discord.Embed(title="VOID ESPORTS™ 6Mans", description=notfull, color=0x00FFFF)
            await ctx.send(embed=embed)
            return
        if self.busy:
            busy = ("Bot is busy. Please wait until picking is done.")
            embed = discord.Embed(title="VOID ESPORTS™ 6Mans", description=busy, color=0x00FFFF)
            await ctx.send(embed=embed)
            return
        self.busy = True
        await self.create_game(ctx)
        team_size = await self.config.guild(ctx.guild).team_size()
        sizes = round(team_size/2)
        orange = random.sample(self.game.players, sizes)
        for player in orange:
            self.game.add_to_orange(player)

        blue = list(self.game.players)
        for player in blue:
            self.game.add_to_blue(player)

        await self.display_teams(ctx)

        self.busy = False

    async def display_teams(self, ctx):
        embed = discord.Embed(title="VOID ESPORTS™ 6Mans", color=0x00FFFF)
        blue = ("🔷 BLUE 🔷: **{}**".format(", ".join([player.display_name for player in self.game.blue])))
        orange = ("🔶 ORANGE 🔶: **{}**".format(", ".join([player.display_name for player in self.game.orange])))
        next_game_number = await self.config.guild(ctx.guild).latest_game_number() + 1
        embed.add_field(name="**Blue Team:**", value=blue, inline=False)
        embed.add_field(name="**Orange Team:**", value=orange, inline=False)
        embed.add_field(name="**Game Code:**", value=next_game_number, inline=False)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/648743379252805663/684605565946953744/octopus-1.png")
        await ctx.send(embed=embed)

        async with self.config.guild(ctx.guild).latest_game_number.get_lock():
            next_game_number = await self.config.guild(ctx.guild).latest_game_number() + 1
            await self.config.custom("GAMES", ctx.guild.id, next_game_number).blue.set([player.id for player in self.game.blue])
            await self.config.custom("GAMES", ctx.guild.id, next_game_number).orange.set([player.id for player in self.game.orange])
            await self.config.guild(ctx.guild).latest_game_number.set(next_game_number)

    async def create_game(self, ctx):
        team_size = await self.config.guild(ctx.guild).team_size()
        players = [self.queue.get() for _ in range(team_size)]
        self.game = Game(players)

    @commands.command(aliases=["smr"])
    async def smreport(self, ctx, code: int, winorloss):
        """Command to report game results."""
        if winorloss != "win":
            if winorloss != "loss":
                await ctx.send("Please use either win or loss")
                return
        orange = await self.config.custom("GAMES", ctx.guild.id, code).orange()
        blue = await self.config.custom("GAMES", ctx.guild.id, code).blue()
        if blue is None:
            await ctx.send("That code doesn't exist")
            return
        orange = await self.config.custom("GAMES", ctx.guild.id, code).orange()
        blue = await self.config.custom("GAMES", ctx.guild.id, code).blue()
        if orange == "Fin":
            await ctx.send("This game has already been reported.")
            return
        for users in orange:
            user = ctx.guild.get_member(users)
            if ctx.author.id in orange:
                wins = await self.config.user(user).wins()
                losses = await self.config.user(user).losses()
                if winorloss == "win":
                    new_win = wins + 1
                    if losses == 0:
                        winloss = 100
                    else:
                        new = losses + new_win
                        winloss = round(new_win / new * 100, 2)
                    await self.config.user(user).wins.set(new_win)
                    await self.config.user(user).winloss.set(winloss)
                    report = ("**{}** now has **{wins} win/s**. **{losses} loss/es** and a win/loss of **{winloss}%**".format(user.mention, wins=new_win, losses=losses, winloss=winloss))
                    embed = discord.Embed(title="VOID ESPORTS™ 6Mans", description=report, color=0x00FFFF)
                    await ctx.send(embed=embed)
                    await self.config.custom("GAMES", ctx.guild.id, code).orange.set("Fin")
                else:
                    new_loss = losses + 1
                    new = wins + new_loss
                    winloss = round(wins / new * 100, 2)
                    await self.config.user(user).losses.set(new_loss)
                    await self.config.user(user).winloss.set(winloss)
                    report = ("**{}** now has **{wins} win/s**, **{losses} loss/es** and a win/loss of **{winloss}%**".format(user.mention, wins=wins, losses=new_loss, winloss=winloss))
                    embed = discord.Embed(title="VOID ESPORTS™ 6Mans", description=report, color=0x00FFFF)
                    await ctx.send(embed=embed)
                    await self.config.custom("GAMES", ctx.guild.id, code).orange.set("Fin")
        for users in blue:
            user = ctx.guild.get_member(users)
            if ctx.author.id in blue:
                wins = await self.config.user(user).wins()
                losses = await self.config.user(user).losses()
                if winorloss == "win":
                    new_win = wins + 1
                    if losses == 0:
                        winloss = 100
                    else:
                        new = losses + new_win
                        winloss = round(new_win / new * 100, 2)
                    await self.config.user(user).wins.set(new_win)
                    await self.config.user(user).winloss.set(winloss)
                    report = ("**{}** now has **{wins} win/s**, **{losses} loss/es** and a win/loss of **{winloss}%**".format(user.mention, wins=new_win, losses=losses, winloss=winloss))
                    embed = discord.Embed(title="VOID ESPORTS™ 6Mans", description=report, color=0x00FFFF)
                    await ctx.send(embed=embed)
                    await self.config.custom("GAMES", ctx.guild.id, code).orange.set("Fin")
                else:
                    new_loss = losses + 1
                    new = wins + new_loss
                    winloss = round(wins / new * 100, 2)
                    await self.config.user(user).losses.set(new_loss)
                    await self.config.user(user).winloss.set(winloss)
                    report = ("**{}** now has **{wins} win/s**, **{losses} loss/es** and a win/loss of **{winloss}%**".format(user.mention, wins=wins, losses=new_loss, winloss=winloss))
                    embed = discord.Embed(title="VOID ESPORTS™ 6Mans", description=report, color=0x00FFFF)
                    await ctx.send(embed=embed)
                    await self.config.custom("GAMES", ctx.guild.id, code).orange.set("Fin")
        if ctx.author.id not in orange:
            if ctx.author.id not in blue:
                await ctx.send("You can't report this game as you are not in it.")

    @commands.command()
    async def smtop(self, ctx):
        """Command to show the 6Mans leaderboard."""
        embeds = []
        msg = ""
        users = await self.config.all_users()
        test = sorted(users, key=lambda a: users[a]['wins'], reverse=True)
        for user in test:
            wins = users[user]['wins']
            losses = users[user]['losses']
            winloss = users[user]['winloss']
            user = ctx.guild.get_member(user)
            msg += (f"{user.display_name}:".ljust(12, ' ')) + (f" Wins: {wins}".ljust(13, ' ')) + (f"Losses: {losses}".ljust(13, ' ')) + f"Win/Loss: {winloss}%\n"
        for msg in pagify(msg):
            embed = discord.Embed(color=0x00FFFF)
            embed.description = box(msg)
            embed.set_author(name="VOID ESPORTS™ 6Mans Leaderboard", icon_url="https://cdn.discordapp.com/attachments/648743379252805663/684605565946953744/octopus-1.png")
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
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

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
