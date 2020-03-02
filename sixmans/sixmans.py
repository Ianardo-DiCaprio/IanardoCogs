import collections
import operator
import random
import time
from queue import Queue

import discord
from redbot.core import commands

team_size = 6

class SixMans:
    def __init__(self, bot):
        self.bot = bot
        self.queue = PlayerQueue()
        self.game = None
        self.busy = False

    # @commands.command(pass_context=True)
    # async def queue_all(self, ctx, *members: discord.Member):
    #     for member in members:
    #         self.queue.put(member)
    #     self.queue.put(ctx.message.author)

    @commands.command(pass_context=True, name="queue", aliases=["q"], description="Add yourself to the queue")
    async def q(self, ctx):
        player = ctx.message.author

        if player in self.queue:
            await self.bot.say("{} is already in queue.".format(player.display_name))
            return
        if self.busy and player in self.game:
            await self.bot.say("{} is already in a game.".format(player.display_name))
            return

        self.queue.put(player)

        await self.bot.say("{} added to queue. ({:d}/{:d})".format(player.display_name, self.queue.qsize(), team_size))
        if self.queue_full():
            self.bot.say("Queue is now full! Type {prefix}captains or {prefix}random to create a game.".format(
                prefix=self.bot.command_prefix))

    @commands.command(pass_context=True, name="dequeue", aliases=["dq"], description="Remove yourself from the queue")
    async def dq(self, ctx):
        player = ctx.message.author

        if player in self.queue:
            self.queue.remove(player)
            await self.bot.say(
                "{} removed from queue. ({:d}/{:d})".format(player.display_name, self.queue.qsize(), team_size))
        else:
            await self.bot.say("{} is not in queue.".format(player.display_name))

    @commands.command(description="Remove someone else from the queue")
    async def kick(self, player: discord.Member):
        if player in self.queue:
            self.queue.remove(player)
            await self.bot.say(
                "{} removed from queue. ({:d}/{:d})".format(player.display_name, self.queue.qsize(), team_size))
        else:
            await self.bot.say("{} is not in queue.".format(player.display_name))

    def queue_full(self):
        return self.queue.qsize() >= team_size

    def check_vote_command(self, message):
        if not message.content.startswith("{prefix}vote".format(prefix=self.bot.command_prefix)):
            return False
        if not len(message.mentions) == 1:
            return False
        return True

    @commands.command(description="Start a game by voting for captains")
    async def voting(self):
        if not self.queue_full():
            await self.bot.say("Queue is not full.")
            return
        if self.busy:
            await self.bot.say("Bot is busy. Please wait until picking is done.")
            return
        self.busy = True
        self.create_game()

        await self.bot.say(
            "Captain voting initiated. Use {prefix}vote [user] to vote for a captain (cannot be yourself).".format(
                prefix=self.bot.command_prefix))
        await self.bot.say("Available: {}".format(", ".join([player.display_name for player in self.game.players])))

        votes = {}
        timeout = 90
        end_time = time.time() + timeout
        while len(votes) < team_size and time.time() < end_time:
            msg = await self.bot.wait_for_message(timeout=1, check=self.check_vote_command)
            if not msg:
                continue
            if msg.author not in self.game.players:
                return

            vote = msg.mentions[0]
            if vote == msg.author:
                await self.bot.say("Cannot vote for yourself.")
            elif vote in self.game.players:
                votes[msg.author] = msg.mentions[0]
                await self.bot.say("Vote added for {}.".format(vote.display_name))
            else:
                await self.bot.say("{} not available to pick.".format(vote.display_name))
        if len(votes) < team_size:
            await self.bot.say("Timed out.")
            msg = ""
            for player in self.game.players:
                if player not in votes:
                    vote = player
                    while vote == player:
                        vote = random.choice(tuple(self.game.players))
                    votes[player] = vote
                    msg += "Random vote added for {} from {}.\n".format(vote.display_name, player.display_name)
            await self.bot.say(msg)

        vote_nums = {}
        for vote in votes.values():
            vote_nums[vote] = vote_nums.get(vote, 0) + 1
        sorted_vote_nums = sorted(vote_nums.items(), key=operator.itemgetter(1), reverse=True)
        top_votes = [key for key, value in sorted_vote_nums if value == sorted_vote_nums[0][1]]
        if len(top_votes) < 2:
            self.game.captains = top_votes
            secondary_votes = [key for key, value in sorted_vote_nums if value == sorted_vote_nums[1][1]]
            if len(secondary_votes) > 1:
                await self.bot.say("{:d}-way tie for 2nd captain. Shuffling picks...".format(len(secondary_votes)))
                random.shuffle(secondary_votes)
            self.game.captains.append(secondary_votes[0])
        else:
            if len(top_votes) > 2:
                await self.bot.say("{:d}-way tie for captains. Shuffling picks...".format(len(top_votes)))
            random.shuffle(top_votes)
            self.game.captains = top_votes[:2]

        await self.do_picks()

        self.busy = False

    def check_orange_first_pick_command(self, message):
        if not message.content.startswith("{prefix}pick".format(prefix=self.bot.command_prefix)):
            return False
        if not len(message.mentions) == 1:
            return False
        return True

    def check_blue_picks_command(self, message):
        if not message.content.startswith("{prefix}pick".format(prefix=self.bot.command_prefix)):
            return False
        if not len(message.mentions) == 2:
            return False
        return True

    @commands.command(description="Start a game by randomly choosing captains")
    async def captains(self):
        if not self.queue_full():
            await self.bot.say("Queue is not full.")
            return
        if self.busy:
            await self.bot.say("Bot is busy. Please wait until picking is done.")
            return
        self.busy = True
        self.create_game()

        await self.do_picks()

        self.busy = False

    async def do_picks(self):
        await self.bot.say("Captains: {} and {}".format(*[captain.mention for captain in self.game.captains]))
        orange_captain = self.game.captains[0]
        self.game.add_to_orange(orange_captain)
        blue_captain = self.game.captains[1]
        self.game.add_to_blue(blue_captain)

        # Orange Pick
        await self.bot.say(
            "{mention} Use {prefix}pick [user] to pick 1 player.".format(mention=orange_captain.mention,
                                                                         prefix=self.bot.command_prefix))
        await self.bot.say("Available: {}".format(", ".join([player.display_name for player in self.game.players])))
        orange_pick = None
        while not orange_pick:
            orange_pick = await self.pick_orange(orange_captain)
        self.game.add_to_orange(orange_pick)

        # Blue Picks
        await self.bot.say(
            "{mention} Use {prefix}pick [user1] [user2] to pick 2 players.".format(mention=blue_captain.mention,
                                                                                   prefix=self.bot.command_prefix))
        await self.bot.say("Available: {}".format(", ".join([player.display_name for player in self.game.players])))
        blue_picks = None
        while not blue_picks:
            blue_picks = await self.pick_blue(blue_captain)
        for blue_pick in blue_picks:
            self.game.add_to_blue(blue_pick)

        # Orange Player
        last_player = next(iter(self.game.players))
        self.game.add_to_orange(last_player)
        await self.bot.say("{} added to 🔶 ORANGE 🔶 team.".format(last_player.mention))
        await self.display_teams()

    async def pick_orange(self, captain):
        msg = await self.bot.wait_for_message(timeout=60, author=captain, check=self.check_orange_first_pick_command)
        if msg:
            pick = msg.mentions[0]
            if pick not in self.game.players:
                await self.bot.say("{} not available to pick.".format(pick.display_name))
                return None
            await self.bot.say("Picked {} for 🔶 ORANGE 🔶 team.".format(pick.mention))
        else:
            pick = random.choice(tuple(self.game.players))
            await self.bot.say("Timed out. Randomly picked {} for 🔶 ORANGE 🔶 team.".format(pick.mention))
        return pick

    async def pick_blue(self, captain):
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

    @commands.command(description="Start a game by randomly assigning teams")
    async def random(self):
        if not self.queue_full():
            await self.bot.say("Queue is not full.")
            return
        if self.busy:
            await self.bot.say("Bot is busy. Please wait until picking is done.")
            return
        self.busy = True
        self.create_game()

        orange = random.sample(self.game.players, 3)
        for player in orange:
            self.game.add_to_orange(player)

        blue = list(self.game.players)
        for player in blue:
            self.game.add_to_blue(player)

        await self.display_teams()

        self.busy = False

    async def display_teams(self):
        await self.bot.say("🔶 ORANGE 🔶: {}".format(", ".join([player.display_name for player in self.game.orange])))
        await self.bot.say("🔷 BLUE 🔷: {}".format(", ".join([player.display_name for player in self.game.blue])))

    def create_game(self):
        players = [self.queue.get() for _ in range(team_size)]
        self.game = Game(players)


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
