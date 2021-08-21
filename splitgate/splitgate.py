import discord
import aiohttp
from redbot.core import commands, checks, Config
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from redbot.core.utils.chat_formatting import pagify
from typing import Optional

class SPLITGATE(commands.Cog):
    """"Simple Commands to get stats for Splitgate"""

    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, identifier=699113442013)

        self._session = aiohttp.ClientSession()

        default_user = {
            "platform": None,
            "username": None,
        }
        default_global = {
            "apikey": None
        }

        self.conf.register_user(**default_user)
        self.conf.register_global(**default_global)

    def cog_unload(self):
        self.bot.loop.create_task(self._session.close())

    @commands.command()
    async def splitgatepset(self, ctx, platform=None):
        """Command to set Splitgate platform"""
        if platform:
            await self.conf.user(ctx.author).platform.set(platform)
            await ctx.send("Your platform has been set.")
        else:
            await self.conf.user(ctx.author).platform.set(platform)
            await ctx.send("Your platform has been removed.")

    @commands.command()
    async def splitgateuset(self, ctx, username=None):
        """Command to set Splitgate username"""
        if username:
            await self.conf.user(ctx.author).username.set(username)
            await ctx.send("Your username has been set.")
        else:
            await self.conf.user(ctx.author).username.set(username)
            await ctx.send("Your username has been removed.")

    @commands.command()
    async def splitgateapiset(self, ctx, api=None):
        """Command to set Splitgate api"""
        if api:
            await self.conf.apikey.set(api)
            await ctx.send("Your API has been set.")
        else:
            await self.conf.apikey.set(api)
            await ctx.send("Your API has been removed.")

    @commands.command()
    async def splitgatestats(self, ctx, platform: Optional[str] = "", *, username: Optional[str] = ""):
        """Command to get your Splitgate stats
        For platform use pc, xbox, psn"""
        embeds = []
        if platform + username == "":
            user = ctx.author
            platform = await self.conf.user(user).platform()
            username = await self.conf.user(user).username()
        username = username.replace(" ", "%20")
        platform = platform.replace("xbox", "xbl")
        apikey = await self.conf.apikey()
        headers = {'TRN-Api-Key':f'{apikey}'}
        async with self._session.get(
                f"https://public-api.tracker.gg/v2/splitgate/standard/profile/{platform}/{username}",headers=headers
            ) as request:
                data = await request.json()
        #Page 1
        try:
            if data["data"]["platformInfo"]["platformUserHandle"] != "N/A":
                username = data["data"]["platformInfo"]["platformUserHandle"]
            embed = discord.Embed(title=f"Splitgate Stats - {username}", color=0x8C05D2)
            embed.set_thumbnail(url=data["data"]["segments"][0]["stats"]["rankLevel"]["metadata"]["imageUrl"])
            embed.set_footer(text="React to change pages for more stats! **Page 1 of 7**")
            if data["data"]["segments"][0]["stats"]["firstBloods"]["value"] != "N/A":
                firstBloods = data["data"]["segments"][0]["stats"]["firstBloods"]["value"]
                embed.add_field(name="**First Bloods:**", value=firstBloods, inline=True)
            if data["data"]["segments"][0]["stats"]["kills"]["value"] != "N/A":
                kills = data["data"]["segments"][0]["stats"]["kills"]["value"]
                embed.add_field(name="**kills:**", value=kills, inline=True)
            if data["data"]["segments"][0]["stats"]["assists"]["value"] != "N/A":
                assists = data["data"]["segments"][0]["stats"]["assists"]["value"]
                embed.add_field(name="**Assists:**", value=assists, inline=True)
            if data["data"]["segments"][0]["stats"]["deaths"]["value"] != "N/A":
                deaths = data["data"]["segments"][0]["stats"]["deaths"]["value"]
                embed.add_field(name="**Deaths:**", value=deaths, inline=True)
            if data["data"]["segments"][0]["stats"]["suicides"]["value"] != "N/A":
                suicides = data["data"]["segments"][0]["stats"]["suicides"]["value"]
                embed.add_field(name="**Suicides:**", value=suicides, inline=True)
            if data["data"]["segments"][0]["stats"]["meleeKills"]["value"] != "N/A":
                meleeKills = data["data"]["segments"][0]["stats"]["meleeKills"]["value"]
                embed.add_field(name="**Melee Kills:**", value=meleeKills, inline=True)
            if data["data"]["segments"][0]["stats"]["portalKills"]["value"] != "N/A":
                portalKills = data["data"]["segments"][0]["stats"]["portalKills"]["value"]
                embed.add_field(name="**Portal Kills:**", value=portalKills, inline=True)
            if data["data"]["segments"][0]["stats"]["killsThruPortal"]["value"] != "N/A":
                killsThruPortal = data["data"]["segments"][0]["stats"]["killsThruPortal"]["value"]
                embed.add_field(name="**Kills Thru Portal:**", value=killsThruPortal, inline=True)
            if data["data"]["segments"][0]["stats"]["headshotsLanded"]["value"] != "N/A":
                headshotsLanded = data["data"]["segments"][0]["stats"]["headshotsLanded"]["value"]
                embed.add_field(name="**Headshots Landed:**", value=headshotsLanded, inline=True)
            if data["data"]["segments"][0]["stats"]["headshotKills"]["value"] != "N/A":
                headshotKills = data["data"]["segments"][0]["stats"]["headshotKills"]["value"]
                embed.add_field(name="**Headshot Kills:**", value=headshotKills, inline=True)
            if data["data"]["segments"][0]["stats"]["collaterals"]["value"] != "N/A":
                collaterals = data["data"]["segments"][0]["stats"]["collaterals"]["value"]
                embed.add_field(name="**Collaterals:**", value=collaterals, inline=True)
            if data["data"]["segments"][0]["stats"]["kingSlayers"]["value"] != "N/A":
                kingSlayers = data["data"]["segments"][0]["stats"]["kingSlayers"]["value"]
                embed.add_field(name="**King Slayers:**", value=kingSlayers, inline=True)
            if data["data"]["segments"][0]["stats"]["revengeKills"]["value"] != "N/A":
                revengeKills = data["data"]["segments"][0]["stats"]["revengeKills"]["value"]
                embed.add_field(name="**Revenge Kills:**", value=revengeKills, inline=True)
            embeds.append(embed)

            if data["data"]["platformInfo"]["platformUserHandle"] != "N/A":
                username = data["data"]["platformInfo"]["platformUserHandle"]
            embed = discord.Embed(title=f"Splitgate Stats - {username}", color=0x8C05D2)
            embed.set_thumbnail(url=data["data"]["segments"][0]["stats"]["rankLevel"]["metadata"]["imageUrl"])
            embed.set_footer(text="React to change pages for more stats! **Page 2 of 7**")
            if data["data"]["segments"][0]["stats"]["rankLevel"]["metadata"]["rankName"] != "N/A":
                rankLevel = data["data"]["segments"][0]["stats"]["rankLevel"]["metadata"]["rankName"]
                embed.add_field(name="**Rank:**", value=rankLevel, inline=True)
            if data["data"]["segments"][0]["stats"]["rankLevel"]["percentile"] != "N/A":
                percentile = data["data"]["segments"][0]["stats"]["rankLevel"]["percentile"]
                embed.add_field(name="**Rank Percentile**", value=percentile, inline=True)
            if data["data"]["segments"][0]["stats"]["rankProgression"]["displayValue"] != "N/A":
                rankProgression = data["data"]["segments"][0]["stats"]["rankProgression"]["displayValue"]
                embed.add_field(name="**Rank Progression**", value=rankProgression, inline=True)
            if data["data"]["segments"][0]["stats"]["portalsSpawned"]["value"] != "N/A":
                portalsSpawned = data["data"]["segments"][0]["stats"]["portalsSpawned"]["value"]
                embed.add_field(name="**Portals Spawned**", value=portalsSpawned, inline=True)
            if data["data"]["segments"][0]["stats"]["ownPortalsEntered"]["value"] != "N/A":
                ownPortalsEntered = data["data"]["segments"][0]["stats"]["ownPortalsEntered"]["value"]
                embed.add_field(name="**Own Portals Entered**", value=ownPortalsEntered, inline=True)
            if data["data"]["segments"][0]["stats"]["allyPortalsEntered"]["value"] != "N/A":
                allyPortalsEntered = data["data"]["segments"][0]["stats"]["allyPortalsEntered"]["value"]
                embed.add_field(name="**Ally Portals Entered**", value=allyPortalsEntered, inline=True)
            if data["data"]["segments"][0]["stats"]["enemyPortalsEntered"]["value"] != "N/A":
                enemyPortalsEntered = data["data"]["segments"][0]["stats"]["enemyPortalsEntered"]["value"]
                embed.add_field(name="**Enemy Portals Entered**", value=enemyPortalsEntered, inline=True)
            if data["data"]["segments"][0]["stats"]["distancePortaled"]["value"] != "N/A":
                distancePortaled = data["data"]["segments"][0]["stats"]["distancePortaled"]["value"]
                embed.add_field(name="**Distance Portaled**", value=distancePortaled, inline=True)
            if data["data"]["segments"][0]["stats"]["enemyPortalsDestroyed"]["value"] != "N/A":
                enemyPortalsDestroyed = data["data"]["segments"][0]["stats"]["enemyPortalsDestroyed"]["value"]
                embed.add_field(name="**Enemy Portals Destroyed**", value=enemyPortalsDestroyed, inline=True)
            embeds.append(embed)

            if data["data"]["platformInfo"]["platformUserHandle"] != "N/A":
                username = data["data"]["platformInfo"]["platformUserHandle"]
            embed = discord.Embed(title=f"Splitgate Stats - {username}", color=0x8C05D2)
            embed.set_thumbnail(url=data["data"]["segments"][0]["stats"]["rankLevel"]["metadata"]["imageUrl"])
            embed.set_footer(text="React to change pages for more stats! **Page 3 of 7**")
            if data["data"]["segments"][0]["stats"]["headshotAccuracy"]["displayValue"] != "N/A":
                headshotAccuracy = data["data"]["segments"][0]["stats"]["headshotAccuracy"]["displayValue"]
                embed.add_field(name="**Headshot Accuracy:**", value=headshotAccuracy, inline=True)
            if data["data"]["segments"][0]["stats"]["shotsAccuracy"]["displayValue"] != "N/A":
                shotsAccuracy = data["data"]["segments"][0]["stats"]["shotsAccuracy"]["displayValue"]
                embed.add_field(name="**Accuracy:**", value=shotsAccuracy, inline=True)
            if data["data"]["segments"][0]["stats"]["shotsFired"]["value"] != "N/A":
                shotsFired = data["data"]["segments"][0]["stats"]["shotsFired"]["value"]
                embed.add_field(name="**Shots Fired:**", value=shotsFired, inline=True)
            if data["data"]["segments"][0]["stats"]["shotsLanded"]["value"] != "N/A":
                shotsLanded = data["data"]["segments"][0]["stats"]["shotsLanded"]["value"]
                embed.add_field(name="**Shots Landed:**", value=shotsLanded, inline=True)
            if data["data"]["segments"][0]["stats"]["kd"]["value"] != "N/A":
                kd = data["data"]["segments"][0]["stats"]["kd"]["value"]
                embed.add_field(name="**K/D:**", value=kd, inline=True)
            if data["data"]["segments"][0]["stats"]["kad"]["value"] != "N/A":
                kad = data["data"]["segments"][0]["stats"]["kad"]["value"]
                embed.add_field(name="**KA/D:**", value=kad, inline=True)
            if data["data"]["segments"][0]["stats"]["killsPerMinute"]["value"] != "N/A":
                killsPerMinute = data["data"]["segments"][0]["stats"]["killsPerMinute"]["value"]
                embed.add_field(name="**Kills Per Minute:**", value=killsPerMinute, inline=True)
            if data["data"]["segments"][0]["stats"]["killsPerMatch"]["value"] != "N/A":
                killsPerMatch = data["data"]["segments"][0]["stats"]["killsPerMatch"]["value"]
                embed.add_field(name="**Kills Per Match:**", value=killsPerMatch, inline=True)
            if data["data"]["segments"][0]["stats"]["teabags"]["value"] != "N/A":
                teabags = data["data"]["segments"][0]["stats"]["teabags"]["value"]
                embed.add_field(name="**Teabags:**", value=teabags, inline=True)
            embeds.append(embed)

            if data["data"]["platformInfo"]["platformUserHandle"] != "N/A":
                username = data["data"]["platformInfo"]["platformUserHandle"]
            embed = discord.Embed(title=f"Splitgate Stats - {username}", color=0x8C05D2)
            embed.set_thumbnail(url=data["data"]["segments"][0]["stats"]["rankLevel"]["metadata"]["imageUrl"])
            embed.set_footer(text="React to change pages for more stats! **Page 4 of 7**")
            if data["data"]["segments"][0]["stats"]["progressionXp"]["value"] != "N/A":
                progressionXp = data["data"]["segments"][0]["stats"]["progressionXp"]["value"]
                embed.add_field(name="**Total XP:**", value=progressionXp, inline=True)
            if data["data"]["segments"][0]["stats"]["progressionXp"]["value"] != "N/A":
                progressionXp = data["data"]["segments"][0]["stats"]["progressionXp"]["value"]
                embed.add_field(name="**Total XP:**", value=progressionXp, inline=True)
            if data["data"]["segments"][0]["stats"]["timePlayed"]["displayValue"] != "N/A":
                timePlayed = data["data"]["segments"][0]["stats"]["timePlayed"]["displayValue"]
                embed.add_field(name="**Time Played:**", value=timePlayed, inline=True)
            if data["data"]["segments"][0]["stats"]["matchesPlayed"]["value"] != "N/A":
                matchesPlayed = data["data"]["segments"][0]["stats"]["matchesPlayed"]["value"]
                embed.add_field(name="**Matches Played:**", value=matchesPlayed, inline=True)
            if data["data"]["segments"][0]["stats"]["damageDealt"]["value"] != "N/A":
                damageDealt = data["data"]["segments"][0]["stats"]["damageDealt"]["value"]
                embed.add_field(name="**Damage Dealt:**", value=damageDealt, inline=True)
            if data["data"]["segments"][0]["stats"]["wins"]["value"] != "N/A":
                wins = data["data"]["segments"][0]["stats"]["wins"]["value"]
                embed.add_field(name="**Wins:**", value=wins, inline=True)
            if data["data"]["segments"][0]["stats"]["losses"]["value"] != "N/A":
                losses = data["data"]["segments"][0]["stats"]["losses"]["value"]
                embed.add_field(name="**Losses:**", value=losses, inline=True)
            if data["data"]["segments"][0]["stats"]["wlPercentage"]["value"] != "N/A":
                wlPercentage = data["data"]["segments"][0]["stats"]["wlPercentage"]["value"]
                embed.add_field(name="**Win/Loss Percent:**", value=f"{wlPercentage}%", inline=True)
            embeds.append(embed)

            if data["data"]["platformInfo"]["platformUserHandle"] != "N/A":
                username = data["data"]["platformInfo"]["platformUserHandle"]
            embed = discord.Embed(title=f"Splitgate Stats - {username}", color=0x8C05D2)
            embed.set_thumbnail(url=data["data"]["segments"][0]["stats"]["rankLevel"]["metadata"]["imageUrl"])
            embed.set_footer(text="React to change pages for more stats! **Page 5 of 7**")
            if data["data"]["segments"][0]["stats"]["medalDoubleKills"]["value"] != "N/A":
                medalDoubleKills = data["data"]["segments"][0]["stats"]["medalDoubleKills"]["value"]
                embed.add_field(name="**Double Kills:**", value=medalDoubleKills, inline=True)
            if data["data"]["segments"][0]["stats"]["medalTripleKills"]["value"] != "N/A":
                medalTripleKills = data["data"]["segments"][0]["stats"]["medalTripleKills"]["value"]
                embed.add_field(name="**Triple Kills:**", value=medalTripleKills, inline=True)
            if data["data"]["segments"][0]["stats"]["medalQuadKills"]["value"] != "N/A":
                medalQuadKills = data["data"]["segments"][0]["stats"]["medalQuadKills"]["value"]
                embed.add_field(name="**Quad Kills:**", value=medalQuadKills, inline=True)
            if data["data"]["segments"][0]["stats"]["medalQuintKills"]["value"] != "N/A":
                medalQuintKills = data["data"]["segments"][0]["stats"]["medalQuintKills"]["value"]
                embed.add_field(name="**Quint Kills:**", value=medalQuintKills, inline=True)
            if data["data"]["segments"][0]["stats"]["medalSexKills"]["value"] != "N/A":
                medalSexKills = data["data"]["segments"][0]["stats"]["medalSexKills"]["value"]
                embed.add_field(name="**Sex Kills:**", value=medalSexKills, inline=True)
            embeds.append(embed)

            if data["data"]["platformInfo"]["platformUserHandle"] != "N/A":
                username = data["data"]["platformInfo"]["platformUserHandle"]
            embed = discord.Embed(title=f"Splitgate Stats - {username}", color=0x8C05D2)
            embed.set_thumbnail(url=data["data"]["segments"][0]["stats"]["rankLevel"]["metadata"]["imageUrl"])
            embed.set_footer(text="React to change pages for more stats! **Page 6 of 7**")
            if data["data"]["segments"][0]["stats"]["medalKillstreak1"]["value"] != "N/A":
                medalKillstreak1 = data["data"]["segments"][0]["stats"]["medalKillstreak1"]["value"]
                embed.add_field(name="**5 Killstreaks:**", value=medalKillstreak1, inline=True)
            if data["data"]["segments"][0]["stats"]["medalKillstreak2"]["value"] != "N/A":
                medalKillstreak2 = data["data"]["segments"][0]["stats"]["medalKillstreak2"]["value"]
                embed.add_field(name="**10 Killstreaks:**", value=medalKillstreak2, inline=True)
            if data["data"]["segments"][0]["stats"]["medalKillstreak3"]["value"] != "N/A":
                medalKillstreak3 = data["data"]["segments"][0]["stats"]["medalKillstreak3"]["value"]
                embed.add_field(name="**15 Killstreaks:**", value=medalKillstreak3, inline=True)
            if data["data"]["segments"][0]["stats"]["medalKillstreak4"]["value"] != "N/A":
                medalKillstreak4 = data["data"]["segments"][0]["stats"]["medalKillstreak4"]["value"]
                embed.add_field(name="**20 Killstreaks:**", value=medalKillstreak4, inline=True)
            if data["data"]["segments"][0]["stats"]["medalKillstreak5"]["value"] != "N/A":
                medalKillstreak5 = data["data"]["segments"][0]["stats"]["medalKillstreak5"]["value"]
                embed.add_field(name="**25 Killstreaks:**", value=medalKillstreak5, inline=True)
            if data["data"]["segments"][0]["stats"]["medalKillstreak6"]["value"] != "N/A":
                medalKillstreak6 = data["data"]["segments"][0]["stats"]["medalKillstreak6"]["value"]
                embed.add_field(name="**50 Killstreaks:**", value=medalKillstreak6, inline=True)
            embeds.append(embed)

            if data["data"]["platformInfo"]["platformUserHandle"] != "N/A":
                username = data["data"]["platformInfo"]["platformUserHandle"]
            embed = discord.Embed(title=f"Splitgate Stats - {username}", color=0x8C05D2)
            embed.set_thumbnail(url=data["data"]["segments"][0]["stats"]["rankLevel"]["metadata"]["imageUrl"])
            embed.set_footer(text="React to change pages for more stats! **Page 7 of 7**")
            if data["data"]["segments"][0]["stats"]["teabagsDenied"]["value"] != "N/A":
                teabagsDenied = data["data"]["segments"][0]["stats"]["teabagsDenied"]["value"]
                embed.add_field(name="**Teabags Denied:**", value=teabagsDenied, inline=True)
            if data["data"]["segments"][0]["stats"]["oddballsPickedUp"]["value"] != "N/A":
                oddballsPickedUp = data["data"]["segments"][0]["stats"]["oddballsPickedUp"]["value"]
                embed.add_field(name="**Oddballs Picked Up:**", value=oddballsPickedUp, inline=True)
            if data["data"]["segments"][0]["stats"]["oddballKills"]["value"] != "N/A":
                oddballKills = data["data"]["segments"][0]["stats"]["oddballKills"]["value"]
                embed.add_field(name="**Oddball Kills:**", value=oddballKills, inline=True)
            if data["data"]["segments"][0]["stats"]["oddballCarrierKills"]["value"] != "N/A":
                oddballCarrierKills = data["data"]["segments"][0]["stats"]["oddballCarrierKills"]["value"]
                embed.add_field(name="**Oddball Carrier Kills:**", value=oddballCarrierKills, inline=True)
            if data["data"]["segments"][0]["stats"]["killsOnHill"]["value"] != "N/A":
                killsOnHill = data["data"]["segments"][0]["stats"]["killsOnHill"]["value"]
                embed.add_field(name="**Kills On Hill:**", value=killsOnHill, inline=True)
            if data["data"]["segments"][0]["stats"]["killsAsVIP"]["value"] != "N/A":
                killsAsVIP = data["data"]["segments"][0]["stats"]["killsAsVIP"]["value"]
                embed.add_field(name="**Kills As VIP:**", value=killsAsVIP, inline=True)
            if data["data"]["segments"][0]["stats"]["hillsNeutralized"]["value"] != "N/A":
                hillsNeutralized = data["data"]["segments"][0]["stats"]["hillsNeutralized"]["value"]
                embed.add_field(name="**Hills Neutralized:**", value=hillsNeutralized, inline=True)
            if data["data"]["segments"][0]["stats"]["hillsCaptured"]["value"] != "N/A":
                hillsCaptured = data["data"]["segments"][0]["stats"]["hillsCaptured"]["value"]
                embed.add_field(name="**Hills Captured:**", value=hillsCaptured, inline=True)
            if data["data"]["segments"][0]["stats"]["highestConsecutiveKills"]["value"] != "N/A":
                highestConsecutiveKills = data["data"]["segments"][0]["stats"]["highestConsecutiveKills"]["value"]
                embed.add_field(name="**Highest Consecutive Kills:**", value=highestConsecutiveKills, inline=True)
            if data["data"]["segments"][0]["stats"]["flagsReturned"]["value"] != "N/A":
                flagsReturned = data["data"]["segments"][0]["stats"]["flagsReturned"]["value"]
                embed.add_field(name="**Flags Returned:**", value=flagsReturned, inline=True)
            if data["data"]["segments"][0]["stats"]["flagsPickedUp"]["value"] != "N/A":
                flagsPickedUp = data["data"]["segments"][0]["stats"]["flagsPickedUp"]["value"]
                embed.add_field(name="**Flags Picked Up:**", value=flagsPickedUp, inline=True)
            if data["data"]["segments"][0]["stats"]["flagKills"]["value"] != "N/A":
                flagKills = data["data"]["segments"][0]["stats"]["flagKills"]["value"]
                embed.add_field(name="**Flag Kills:**", value=flagKills, inline=True)
            if data["data"]["segments"][0]["stats"]["flagCarrierKills"]["value"] != "N/A":
                flagCarrierKills = data["data"]["segments"][0]["stats"]["flagCarrierKills"]["value"]
                embed.add_field(name="**Flag Carrier Kills:**", value=flagCarrierKills, inline=True)
            if data["data"]["segments"][0]["stats"]["enemyKillsOnHill"]["value"] != "N/A":
                enemyKillsOnHill = data["data"]["segments"][0]["stats"]["enemyKillsOnHill"]["value"]
                embed.add_field(name="**Enemy Kills On Hill:**", value=enemyKillsOnHill, inline=True)
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=180)
        except:
            await ctx.send("Either the platform or username is incorrect, please make sure to use pc, psn or xbox for the platform and make sure you spelt your name correctly.")
