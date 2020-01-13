import discord
import aiohttp
from redbot.core import commands, checks, Config
from redbot.core.utils.menus import menu, DEFAULT_CONTROLS
from redbot.core.utils.chat_formatting import pagify
from typing import Optional

class CODSTATS(commands.Cog):
    """"Simple Commands to get stats for COD"""

    def __init__(self, bot):
        self.bot = bot
        self.conf = Config.get_conf(self, identifier=6991142013)

        self._session = aiohttp.ClientSession()

        default_user = {
            "platform": None,
            "username": None,
        }

        self.conf.register_user(**default_user)

    def cog_unload(self):
        self.bot.loop.create_task(self._session.close())

    @commands.command()
    async def codpset(self, ctx, platform=None):
        """Command to set COD platform"""
        if platform:
            await self.conf.user(ctx.author).platform.set(platform)
            await ctx.send("Your platform has been set.")
        else:
            await self.conf.user(ctx.author).platform.set(platform)
            await ctx.send("Your platform has been removed.")

    @commands.command()
    async def coduset(self, ctx, username=None):
        """Command to set COD username"""
        if username:
            await self.conf.user(ctx.author).username.set(username)
            await ctx.send("Your username has been set.")
        else:
            await self.conf.user(ctx.author).username.set(username)
            await ctx.send("Your username has been removed.")

    @commands.command()
    async def codstats(self, ctx, platform: Optional[str] = "", *, username: Optional[str] = ""):
        """Command to get your COD: MW stats
        For platform use pc, xbox, psn"""
        embeds = []
        if platform + username == "":
            user = ctx.author
            platform = await self.conf.user(user).platform()
            username = await self.conf.user(user).username()
        username = username.replace(" ", "%20")
        username = username.replace("#", "%23")
        platform = platform.replace("pc", "battle")
        platform = platform.replace("xbox", "xbl")
        async with self._session.get(
                f"https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/{platform}/gamer/{username}/profile/type/mp"
            ) as request:
                data = await request.json()
        
        try:
            username = data["data"]["username"]
            level = round(data["data"]["level"])
            userlvl = f"{username} - Level: {level}"
            #Career Stats
            embed = discord.Embed(title=userlvl + " - Career Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["all"]["properties"]["totalShots"] != "N/A":
                totalshots = round(data["data"]["lifetime"]["all"]["properties"]["totalShots"])
                embed.add_field(name="**Total Shots**", value=totalshots, inline=True)
            if data["data"]["prestige"] != "N/A":
                prestige = round(data["data"]["prestige"])
                embed.add_field(name="**Prestige**", value=prestige, inline=True)
            if data["data"]["totalXp"] != "N/A":
                totalxp = round(data["data"]["totalXp"])
                embed.add_field(name="**Total XP**", value=totalxp, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["timePlayedTotal"] != "N/A":
                timeplayedtotal = round(data["data"]["lifetime"]["all"]["properties"]["timePlayedTotal"])
                embed.add_field(name="**Total Playtime**", value=timeplayedtotal, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["hits"] != "N/A":
                hits = round(data["data"]["lifetime"]["all"]["properties"]["hits"])
                embed.add_field(name="**Total Hits**", value=hits, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["score"] != "N/A":
                score = round(data["data"]["lifetime"]["all"]["properties"]["score"])
                embed.add_field(name="**Total Score**", value=score, inline=True)
            embeds.append(embed)
            #Game Stats
            embed = discord.Embed(title=userlvl + " - Game Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["all"]["properties"]["wins"] != "N/A":
                wins = round(data["data"]["lifetime"]["all"]["properties"]["wins"])
                embed.add_field(name="**Total Wins**", value=wins, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["losses"] != "N/A":
                losses = round(data["data"]["lifetime"]["all"]["properties"]["losses"])
                embed.add_field(name="**Total Losses**", value=losses, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["winLossRatio"] != "N/A":
                winloss = round(data["data"]["lifetime"]["all"]["properties"]["winLossRatio"], 2)
                embed.add_field(name="**Win/Loss Ratio**", value=winloss, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["gamesPlayed"] != "N/A":
                gamesplayed = round(data["data"]["lifetime"]["all"]["properties"]["gamesPlayed"])
                embed.add_field(name="**Total Games Played**", value=gamesplayed, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["kills"] != "N/A":
                kills = round(data["data"]["lifetime"]["all"]["properties"]["kills"])
                embed.add_field(name="**Total Kills**", value=kills, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["deaths"] != "N/A":
                deaths = round(data["data"]["lifetime"]["all"]["properties"]["deaths"])
                embed.add_field(name="**Total Deaths**", value=deaths, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["kdRatio"] != "N/A":
                killdeath = round(data["data"]["lifetime"]["all"]["properties"]["kdRatio"], 2)
                embed.add_field(name="**kill/Death Ratio**", value=killdeath, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["assists"] != "N/A":
                assists = round(data["data"]["lifetime"]["all"]["properties"]["assists"])
                embed.add_field(name="**Total Assists**", value=assists, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["headshots"] != "N/A":
                headshots = round(data["data"]["lifetime"]["all"]["properties"]["headshots"])
                embed.add_field(name="**Total headshots**", value=headshots, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["scorePerGame"] != "N/A":
                scoregame = round(data["data"]["lifetime"]["all"]["properties"]["scorePerGame"], 2)
                embed.add_field(name="**Score Per Game**", value=scoregame, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["bestKills"] != "N/A":
                bestkills = round(data["data"]["lifetime"]["all"]["properties"]["bestKills"])
                embed.add_field(name="**Highest Kills**", value=bestkills, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["currentWinStreak"] != "N/A":
                curwinstreak = round(data["data"]["lifetime"]["all"]["properties"]["currentWinStreak"])
                embed.add_field(name="**Current Win Streak**", value=curwinstreak, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["recordLongestWinStreak"] != "N/A":
                recwinstreak = round(data["data"]["lifetime"]["all"]["properties"]["recordLongestWinStreak"])
                embed.add_field(name="**Highest Win Streak**", value=recwinstreak, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["recordXpInAMatch"] != "N/A":
                recxp = round(data["data"]["lifetime"]["all"]["properties"]["recordXpInAMatch"])
                embed.add_field(name="**Highest Score**", value=recxp, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["recordKillStreak"] != "N/A":
                reckills = round(data["data"]["lifetime"]["all"]["properties"]["recordKillStreak"])
                embed.add_field(name="**Highest None Killsteak Kills**", value=reckills, inline=True)
            embeds.append(embed)
            #killstreak Stats
            embed = discord.Embed(title=userlvl + " - Killstreak Uses", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["radar_drone_overwatch"]["properties"]["uses"] != "N/A":
                radrov = round(data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["radar_drone_overwatch"]["properties"]["uses"])
                embed.add_field(name="**Personal Radar**", value=radrov, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["manual_turret"]["properties"]["uses"] != "N/A":
                mantur = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["manual_turret"]["properties"]["uses"])
                embed.add_field(name="**Shield Turret**", value=mantur, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["scrambler_drone_guard"]["properties"]["uses"] != "N/A":
                scdrgu = round(data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["scrambler_drone_guard"]["properties"]["uses"])
                embed.add_field(name="**Counter UAV**", value=scdrgu, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["uav"]["properties"]["uses"] != "N/A":
                uav = round(data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["uav"]["properties"]["uses"])
                embed.add_field(name="**UAV**", value=uav, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["airdrop"]["properties"]["uses"] != "N/A":
                airdro = round(data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["airdrop"]["properties"]["uses"])
                embed.add_field(name="**Care Package**", value=airdro, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["toma_strike"]["properties"]["uses"] != "N/A":
                tomstri = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["toma_strike"]["properties"]["uses"])
                embed.add_field(name="**Cluster Strike**", value=tomstri, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["cruise_predator"]["properties"]["uses"] != "N/A":
                crupred = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["cruise_predator"]["properties"]["uses"])
                embed.add_field(name="**Cruise Missile**", value=crupred, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["precision_airstrike"]["properties"]["uses"] != "N/A":
                precair = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["precision_airstrike"]["properties"]["uses"])
                embed.add_field(name="**Precision Airstrike**", value=precair, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["pac_sentry"]["properties"]["uses"] != "N/A":
                pacsen = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["pac_sentry"]["properties"]["uses"])
                embed.add_field(name="**Wheelson**", value=pacsen, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["bradley"]["properties"]["uses"] != "N/A":
                bradley = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["bradley"]["properties"]["uses"])
                embed.add_field(name="**Infantry Vehicle**", value=bradley, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["sentry_gun"]["properties"]["uses"] != "N/A":
                sengun = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["sentry_gun"]["properties"]["uses"])
                embed.add_field(name="**Sentry Gun**", value=sengun, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["airdrop_multiple"]["properties"]["uses"] != "N/A":
                airmult = round(data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["airdrop_multiple"]["properties"]["uses"])
                embed.add_field(name="**Emergency Airdrop**", value=airmult, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["hover_jet"]["properties"]["uses"] != "N/A":
                hovjet = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["hover_jet"]["properties"]["uses"])
                embed.add_field(name="**VTOL Jet**", value=hovjet, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["chopper_gunner"]["properties"]["uses"] != "N/A":
                chopgun = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["chopper_gunner"]["properties"]["uses"])
                embed.add_field(name="**Chopper Gunner**", value=chopgun, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["white_phosphorus"]["properties"]["uses"] != "N/A":
                whipho = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["white_phosphorus"]["properties"]["uses"])
                embed.add_field(name="**White Phosphorus**", value=whipho, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["chopper_support"]["properties"]["uses"] != "N/A":
                chopsup = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["chopper_support"]["properties"]["uses"])
                embed.add_field(name="**Support Helo**", value=chopsup, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["gunship"]["properties"]["uses"] != "N/A":
                gunship = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["gunship"]["properties"]["uses"])
                embed.add_field(name="**Gunship**", value=gunship, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["directional_uav"]["properties"]["uses"] != "N/A":
                diruav = round(data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["directional_uav"]["properties"]["uses"])
                embed.add_field(name="**Advanced UAV**", value=diruav, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["juggernaut"]["properties"]["uses"] != "N/A":
                jugger = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["juggernaut"]["properties"]["uses"])
                embed.add_field(name="**Juggernaut**", value=jugger, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["nuke"]["properties"]["uses"] != "N/A":
                nuke = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["nuke"]["properties"]["uses"])
                embed.add_field(name="**Nuke**", value=nuke, inline=True)
            embeds.append(embed)
            #Assault Rifle Stats
            embed = discord.Embed(title=userlvl + " - Assault Rifle Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_kilo433"]["properties"]["kills"] != "N/A":
                kilo = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_kilo433"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_kilo433"]["properties"]["headshots"])
                embed.add_field(name="**Kilo 141 Stats**", value=f"**Kills:** {kilo} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_mike4"]["properties"]["kills"] != "N/A":
                m4a1 = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_mike4"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_mike4"]["properties"]["headshots"])
                embed.add_field(name="**M4A1 Stats**", value=f"**Kills:** {m4a1} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_falpha"]["properties"]["kills"] != "N/A":
                FR = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_falpha"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_falpha"]["properties"]["headshots"])
                embed.add_field(name="**FR 5.56 Stats**", value=f"**Kills:** {FR} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_asierra12"]["properties"]["kills"] != "N/A":
                oden = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_asierra12"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_asierra12"]["properties"]["headshots"])
                embed.add_field(name="**Oden Stats**", value=f"**Kills:** {oden} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_akilo47"]["properties"]["kills"] != "N/A":
                ak = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_akilo47"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_akilo47"]["properties"]["headshots"])
                embed.add_field(name="**AK-47 Stats**", value=f"**Kills:** {ak} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_scharlie"]["properties"]["kills"] != "N/A":
                scar = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_scharlie"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_scharlie"]["properties"]["headshots"])
                embed.add_field(name="**FN Scar 17 Stats**", value=f"**Kills:** {scar} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_falima"]["properties"]["kills"] != "N/A":
                fal = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_falima"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_falima"]["properties"]["headshots"])
                embed.add_field(name="**FAL Stats**", value=f"**Kills:** {fal} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_mcharlie"]["properties"]["kills"] != "N/A":
                m13 = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_mcharlie"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_mcharlie"]["properties"]["headshots"])
                embed.add_field(name="**M13 Stats**", value=f"**Kills:** {m13} \n **headshots:** {headshots}", inline=True)
            embeds.append(embed)
            #LMG Stats
            embed = discord.Embed(title=userlvl + " - LMG Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_kilo121"]["properties"]["kills"] != "N/A":
                m91 = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_kilo121"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_kilo121"]["properties"]["headshots"])
                embed.add_field(name="**M91 Stats**", value=f"**Kills:** {m91} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_lima86"]["properties"]["kills"] != "N/A":
                sa87 = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_lima86"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_lima86"]["properties"]["headshots"])
                embed.add_field(name="**SA87 Stats**", value=f"**Kills:** {sa87} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_mgolf34"]["properties"]["kills"] != "N/A":
                mg34 = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_mgolf34"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_mgolf34"]["properties"]["headshots"])
                embed.add_field(name="**MG34 Stats**", value=f"**Kills:** {mg34} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_pkilo"]["properties"]["kills"] != "N/A":
                pkm = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_pkilo"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_pkilo"]["properties"]["headshots"])
                embed.add_field(name="**PKM Stats**", value=f"**Kills:** {pkm} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_mgolf36"]["properties"]["kills"] != "N/A":
                holger = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_mgolf36"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_mgolf36"]["properties"]["headshots"])
                embed.add_field(name="**Holger-26 Stats**", value=f"**Kills:** {holger} \n **headshots:** {headshots}", inline=True)
            embeds.append(embed)
            #Launcher Stats
            embed = discord.Embed(title=userlvl + " - Launcher Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_gromeo"]["properties"]["kills"] != "N/A":
                pila = round(data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_gromeo"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_gromeo"]["properties"]["headshots"])
                embed.add_field(name="**PILA Stats**", value=f"**Kills:** {pila} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_rpapa7"]["properties"]["kills"] != "N/A":
                rpg = round(data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_rpapa7"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_rpapa7"]["properties"]["headshots"])
                embed.add_field(name="**RPG-7 Stats**", value=f"**Kills:** {rpg} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_juliet"]["properties"]["kills"] != "N/A":
                jokr = round(data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_juliet"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_juliet"]["properties"]["headshots"])
                embed.add_field(name="**JOKR Stats**", value=f"**Kills:** {jokr} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_kgolf"]["properties"]["kills"] != "N/A":
                strella = round(data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_kgolf"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_kgolf"]["properties"]["headshots"])
                embed.add_field(name="**Strella-P Stats**", value=f"**Kills:** {strella} \n **headshots:** {headshots}", inline=True)
            embeds.append(embed)
            #Pistol Stats
            embed = discord.Embed(title=userlvl + " - Pistol Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_decho"]["properties"]["kills"] != "N/A":
                gs = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_decho"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_decho"]["properties"]["headshots"])
                embed.add_field(name="**.50 GS Stats**", value=f"**Kills:** {gs} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_cpapa"]["properties"]["kills"] != "N/A":
                revol = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_cpapa"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_cpapa"]["properties"]["headshots"])
                embed.add_field(name="**.357 Stats**", value=f"**Kills:** {revol} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_mike1911"]["properties"]["kills"] != "N/A":
                m1911 = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_mike1911"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_mike1911"]["properties"]["headshots"])
                embed.add_field(name="**1911 Stats**", value=f"**Kills:** {m1911} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_golf21"]["properties"]["kills"] != "N/A":
                x16 = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_golf21"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_golf21"]["properties"]["headshots"])
                embed.add_field(name="**X16 Stats**", value=f"**Kills:** {x16} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_papa320"]["properties"]["kills"] != "N/A":
                m19 = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_papa320"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_papa320"]["properties"]["headshots"])
                embed.add_field(name="**M19 Stats**", value=f"**Kills:** {m19} \n **headshots:** {headshots}", inline=True)
            embeds.append(embed)
            #Shotgun Stats
            embed = discord.Embed(title=userlvl + " - Shotgun Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_charlie725"]["properties"]["kills"] != "N/A":
                farmer = round(data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_charlie725"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_charlie725"]["properties"]["headshots"])
                embed.add_field(name="**725 Stats**", value=f"**Kills:** {farmer} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_romeo870"]["properties"]["kills"] != "N/A":
                model = round(data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_romeo870"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_romeo870"]["properties"]["headshots"])
                embed.add_field(name="**Model 680 Stats**", value=f"**Kills:** {model} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_oscar12"]["properties"]["kills"] != "N/A":
                origin = round(data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_oscar12"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_oscar12"]["properties"]["headshots"])
                embed.add_field(name="**Origin 12 Shotgun Stats**", value=f"**Kills:** {origin} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_dpapa12"]["properties"]["kills"] != "N/A":
                r9 = round(data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_dpapa12"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_dpapa12"]["properties"]["headshots"])
                embed.add_field(name="**R9-0 Shotgun Stats**", value=f"**Kills:** {r9} \n **headshots:** {headshots}", inline=True)
            embeds.append(embed)
            #SMG Stats
            embed = discord.Embed(title=userlvl + " - SMG Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_mpapa7"]["properties"]["kills"] != "N/A":
                mp7 = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_mpapa7"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_mpapa7"]["properties"]["headshots"])
                embed.add_field(name="**MP7 Stats**", value=f"**Kills:** {mp7} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_augolf"]["properties"]["kills"] != "N/A":
                aug = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_augolf"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_augolf"]["properties"]["headshots"])
                embed.add_field(name="**AUG Stats**", value=f"**Kills:** {aug} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_papa90"]["properties"]["kills"] != "N/A":
                p90 = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_papa90"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_papa90"]["properties"]["headshots"])
                embed.add_field(name="**P90 Stats**", value=f"**Kills:** {p90} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_mpapa5"]["properties"]["kills"] != "N/A":
                mp5 = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_mpapa5"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_mpapa5"]["properties"]["headshots"])
                embed.add_field(name="**MP5 Stats**", value=f"**Kills:** {mp5} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_beta"]["properties"]["kills"] != "N/A":
                bizon = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_beta"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_beta"]["properties"]["headshots"])
                embed.add_field(name="**PP19 Bizon Stats**", value=f"**Kills:** {bizon} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_uzulu"]["properties"]["kills"] != "N/A":
                uzi = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_uzulu"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_uzulu"]["properties"]["headshots"])
                embed.add_field(name="**Uzi Stats**", value=f"**Kills:** {uzi} \n **headshots:** {headshots}", inline=True)
            embeds.append(embed)
            #Sniper Rifle Stats
            embed = discord.Embed(title=userlvl + " - Sniper Rifle Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["weapon_sniper"]["iw8_sn_hdromeo"]["properties"]["kills"] != "N/A":
                hdr = round(data["data"]["lifetime"]["itemData"]["weapon_sniper"]["iw8_sn_hdromeo"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_sniper"]["iw8_sn_hdromeo"]["properties"]["headshots"])
                embed.add_field(name="**HDR Stats**", value=f"**Kills:** {hdr} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_sniper"]["iw8_sn_alpha50"]["properties"]["kills"] != "N/A":
                ax = round(data["data"]["lifetime"]["itemData"]["weapon_sniper"]["iw8_sn_alpha50"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_sniper"]["iw8_sn_alpha50"]["properties"]["headshots"])
                embed.add_field(name="**AX-50 Stats**", value=f"**Kills:** {ax} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_sniper"]["iw8_sn_delta"]["properties"]["kills"] != "N/A":
                drag = round(data["data"]["lifetime"]["itemData"]["weapon_sniper"]["iw8_sn_delta"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_sniper"]["iw8_sn_delta"]["properties"]["headshots"])
                embed.add_field(name="**Dragunov Stats**", value=f"**Kills:** {drag} \n **headshots:** {headshots}", inline=True)
            embeds.append(embed)
            #Marksman Rifle Stats
            embed = discord.Embed(title=userlvl + " - Marksman Rifle Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["weapon_marksman"]["iw8_sn_kilo98"]["properties"]["kills"] != "N/A":
                kar = round(data["data"]["lifetime"]["itemData"]["weapon_marksman"]["iw8_sn_kilo98"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_marksman"]["iw8_sn_kilo98"]["properties"]["headshots"])
                embed.add_field(name="**Kar98K Stats**", value=f"**Kills:** {kar} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_marksman"]["iw8_sn_sbeta"]["properties"]["kills"] != "N/A":
                carbine = round(data["data"]["lifetime"]["itemData"]["weapon_marksman"]["iw8_sn_sbeta"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_marksman"]["iw8_sn_sbeta"]["properties"]["headshots"])
                embed.add_field(name="**MK2 Carbine Stats**", value=f"**Kills:** {carbine} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_marksman"]["iw8_sn_mike14"]["properties"]["kills"] != "N/A":
                ebr = round(data["data"]["lifetime"]["itemData"]["weapon_marksman"]["iw8_sn_mike14"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_marksman"]["iw8_sn_mike14"]["properties"]["headshots"])
                embed.add_field(name="**EBR-14 Stats**", value=f"**Kills:** {ebr} \n **headshots:** {headshots}", inline=True)
            embeds.append(embed)
            #Melee Stats
            embed = discord.Embed(title=userlvl + " - Melee Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["weapon_other"]["iw8_me_riotshield"]["properties"]["hits"] != "N/A":
                riothit = round(data["data"]["lifetime"]["itemData"]["weapon_other"]["iw8_me_riotshield"]["properties"]["hits"])
                riotkill = round(data["data"]["lifetime"]["itemData"]["weapon_other"]["iw8_me_riotshield"]["properties"]["kills"])
                riotob = round(data["data"]["lifetime"]["accoladeData"]["properties"]["riotShieldDamageAbsorbed"])
                embed.add_field(name="**Riotshield Stats**", value=f"**Hits:** {riothit} \n **Kills:** {riotkill} \n **Damage Obsorbed:** {riotob}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_melee"]["iw8_knife"]["properties"]["kills"] != "N/A":
                knifekill = round(data["data"]["lifetime"]["itemData"]["weapon_melee"]["iw8_knife"]["properties"]["kills"])
                embed.add_field(name="**Combat Knife Stats**", value=f"**Kills:** {knifekill}", inline=True)
            embeds.append(embed)
            #Grenade Stats
            embed = discord.Embed(title=userlvl + " - Grenade Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["lethals"]["equip_frag"]["properties"]["kills"] != "N/A":
                frag = round(data["data"]["lifetime"]["itemData"]["lethals"]["equip_frag"]["properties"]["kills"])
                embed.add_field(name="**Frag Grenade Stats**", value=f"**Kills:** {frag}", inline=True)
            if data["data"]["lifetime"]["itemData"]["lethals"]["equip_thermite"]["properties"]["kills"] != "N/A":
                thermite = round(data["data"]["lifetime"]["itemData"]["lethals"]["equip_thermite"]["properties"]["kills"])
                embed.add_field(name="**Thermite Grenade Stats**", value=f"**Kills:** {thermite}", inline=True)
            if data["data"]["lifetime"]["itemData"]["lethals"]["equip_semtex"]["properties"]["kills"] != "N/A":
                semtex = round(data["data"]["lifetime"]["itemData"]["lethals"]["equip_semtex"]["properties"]["kills"])
                embed.add_field(name="**Semtex Grenade Stats**", value=f"**Kills:** {semtex}", inline=True)
            if data["data"]["lifetime"]["itemData"]["lethals"]["equip_claymore"]["properties"]["kills"] != "N/A":
                claymore = round(data["data"]["lifetime"]["itemData"]["lethals"]["equip_claymore"]["properties"]["kills"])
                embed.add_field(name="**Claymore Stats**", value=f"**Kills:** {claymore}", inline=True)
            if data["data"]["lifetime"]["itemData"]["lethals"]["equip_c4"]["properties"]["kills"] != "N/A":
                c4 = round(data["data"]["lifetime"]["itemData"]["lethals"]["equip_c4"]["properties"]["kills"])
                embed.add_field(name="**C4 Stats**", value=f"**Kills:** {c4}", inline=True)
            if data["data"]["lifetime"]["itemData"]["lethals"]["equip_at_mine"]["properties"]["kills"] != "N/A":
                atmine = round(data["data"]["lifetime"]["itemData"]["lethals"]["equip_at_mine"]["properties"]["kills"])
                embed.add_field(name="**Anti-Tank Mine Stats**", value=f"**Kills:** {atmine}", inline=True)
            if data["data"]["lifetime"]["itemData"]["lethals"]["equip_throwing_knife"]["properties"]["kills"] != "N/A":
                throw = round(data["data"]["lifetime"]["itemData"]["lethals"]["equip_throwing_knife"]["properties"]["kills"])
                embed.add_field(name="**Throwing Knife Stats**", value=f"**Kills:** {throw}", inline=True)
            if data["data"]["lifetime"]["itemData"]["lethals"]["equip_molotov"]["properties"]["kills"] != "N/A":
                molotov = round(data["data"]["lifetime"]["itemData"]["lethals"]["equip_molotov"]["properties"]["kills"])
                embed.add_field(name="**Molotov Stats**", value=f"**Kills:** {molotov}", inline=True)
            embeds.append(embed)
            #Domination Stats
            embed = discord.Embed(title=userlvl + " - Domination Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["mode"]["dom"]["properties"]["kills"] != "N/A":
                domkills = round(data["data"]["lifetime"]["mode"]["dom"]["properties"]["kills"])
                domdeaths = round(data["data"]["lifetime"]["mode"]["dom"]["properties"]["deaths"])
                domkd = round(data["data"]["lifetime"]["mode"]["dom"]["properties"]["kdRatio"], 2)
                domscore = round(data["data"]["lifetime"]["mode"]["dom"]["properties"]["score"])
                domcapture = round(data["data"]["lifetime"]["mode"]["dom"]["properties"]["captures"])
                domdef = round(data["data"]["lifetime"]["mode"]["dom"]["properties"]["defends"])
                domscore = round(data["data"]["lifetime"]["mode"]["dom"]["properties"]["score"])
                domspm = round(data["data"]["lifetime"]["mode"]["dom"]["properties"]["scorePerMinute"])
                domtime = round(data["data"]["lifetime"]["mode"]["dom"]["properties"]["timePlayed"])
                embed.add_field(name="**Domination Stats**", value=f"**Kills:** {domkills} \n **Deaths:** {domdeaths} \n **Kill/Death Ratio:** {domkd} \n **Captures:** {domcapture} \n **Defends:** {domdef} \n **Score:** {domscore} \n **Score Per Minute:** {domspm} \n **Time Played:** {domtime}", inline=True)
            if data["data"]["lifetime"]["mode"]["hc_dom"]["properties"]["kills"] != "N/A":
                domkills = round(data["data"]["lifetime"]["mode"]["hc_dom"]["properties"]["kills"])
                domdeaths = round(data["data"]["lifetime"]["mode"]["hc_dom"]["properties"]["deaths"])
                domkd = round(data["data"]["lifetime"]["mode"]["hc_dom"]["properties"]["kdRatio"], 2)
                domscore = round(data["data"]["lifetime"]["mode"]["hc_dom"]["properties"]["score"])
                domcapture = round(data["data"]["lifetime"]["mode"]["hc_dom"]["properties"]["captures"])
                domdef = round(data["data"]["lifetime"]["mode"]["hc_dom"]["properties"]["defends"])
                domscore = round(data["data"]["lifetime"]["mode"]["hc_dom"]["properties"]["score"])
                domspm = round(data["data"]["lifetime"]["mode"]["hc_dom"]["properties"]["scorePerMinute"])
                domtime = round(data["data"]["lifetime"]["mode"]["hc_dom"]["properties"]["timePlayed"])
                embed.add_field(name="**Hardcore Domination Stats**", value=f"**Kills:** {domkills} \n **Deaths:** {domdeaths} \n **Kill/Death Ratio:** {domkd} \n **Captures:** {domcapture} \n **Defends:** {domdef} \n **Score:** {domscore} \n **Score Per Minute:** {domspm} \n **Time Played:** {domtime}", inline=True)
            embeds.append(embed)
            #TeamDeathMatch Stats
            embed = discord.Embed(title=userlvl + " - Team Deathmatch Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["mode"]["war"]["properties"]["kills"] != "N/A":
                tdmkills = round(data["data"]["lifetime"]["mode"]["war"]["properties"]["kills"])
                tdmdeaths = round(data["data"]["lifetime"]["mode"]["war"]["properties"]["deaths"])
                tdmassists = round(data["data"]["lifetime"]["mode"]["war"]["properties"]["assists"])
                tdmkd = round(data["data"]["lifetime"]["mode"]["war"]["properties"]["kdRatio"], 2)
                tdmscore = round(data["data"]["lifetime"]["mode"]["war"]["properties"]["score"])
                tdmspm = round(data["data"]["lifetime"]["mode"]["war"]["properties"]["scorePerMinute"], 2)
                tdmtime = round(data["data"]["lifetime"]["mode"]["war"]["properties"]["timePlayed"])
                embed.add_field(name="**Team Deathmatch Stats**", value=f"**Kills:** {tdmkills} \n **Deaths:** {tdmdeaths} \n **Assists:** {tdmassists} \n **Kill/Death Ratio:** {tdmkd} \n **Score:** {tdmscore} \n **Score Per Minute:** {tdmspm} \n **Time Played:** {tdmtime}", inline=True)
            if data["data"]["lifetime"]["mode"]["hc_war"]["properties"]["kills"] != "N/A":
                tdmkills = round(data["data"]["lifetime"]["mode"]["hc_war"]["properties"]["kills"])
                tdmdeaths = round(data["data"]["lifetime"]["mode"]["hc_war"]["properties"]["deaths"])
                tdmassists = round(data["data"]["lifetime"]["mode"]["hc_war"]["properties"]["assists"])
                tdmkd = round(data["data"]["lifetime"]["mode"]["hc_war"]["properties"]["kdRatio"], 2)
                tdmscore = round(data["data"]["lifetime"]["mode"]["hc_war"]["properties"]["score"])
                tdmspm = round(data["data"]["lifetime"]["mode"]["hc_war"]["properties"]["scorePerMinute"], 2)
                tdmtime = round(data["data"]["lifetime"]["mode"]["hc_war"]["properties"]["timePlayed"])
                embed.add_field(name="**Hardcore Team Deathmatch Stats**", value=f"**Kills:** {tdmkills} \n **Deaths:** {tdmdeaths} \n **Assists:** {tdmassists} \n **Kill/Death Ratio:** {tdmkd} \n **Score:** {tdmscore} \n **Score Per Minute:** {tdmspm} \n **Time Played:** {tdmtime}", inline=True)
            embeds.append(embed)
            #Headquarters Stats
            embed = discord.Embed(title=userlvl + " - Headquarters Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["mode"]["hq"]["properties"]["kills"] != "N/A":
                hqkills = round(data["data"]["lifetime"]["mode"]["hq"]["properties"]["kills"])
                hqdeaths = round(data["data"]["lifetime"]["mode"]["hq"]["properties"]["deaths"])
                hqcap = round(data["data"]["lifetime"]["mode"]["hq"]["properties"]["captures"])
                hqdef = round(data["data"]["lifetime"]["mode"]["hq"]["properties"]["defends"])
                hqkd = round(data["data"]["lifetime"]["mode"]["hq"]["properties"]["kdRatio"], 2)
                hqscore = round(data["data"]["lifetime"]["mode"]["hq"]["properties"]["score"])
                hqspm = round(data["data"]["lifetime"]["mode"]["hq"]["properties"]["scorePerMinute"], 2)
                hqtime = round(data["data"]["lifetime"]["mode"]["hq"]["properties"]["timePlayed"])
                embed.add_field(name="**Headquarters Stats**", value=f"**Kills:** {hqkills} \n **Deaths:** {hqdeaths} \n **Kill/Death Ratio:** {hqkd} \n **Captures:** {hqcap} \n **Defends:** {hqdef} \n **Score:** {hqscore} \n **Score Per Minute:** {hqspm} \n **Time Played:** {hqtime}", inline=True)
            if data["data"]["lifetime"]["mode"]["hc_hq"]["properties"]["kills"] != "N/A":
                hqkills = round(data["data"]["lifetime"]["mode"]["hc_hq"]["properties"]["kills"])
                hqdeaths = round(data["data"]["lifetime"]["mode"]["hc_hq"]["properties"]["deaths"])
                hqcap = round(data["data"]["lifetime"]["mode"]["hc_hq"]["properties"]["captures"])
                hqdef = round(data["data"]["lifetime"]["mode"]["hc_hq"]["properties"]["defends"])
                tdmkd = round(data["data"]["lifetime"]["mode"]["hc_hq"]["properties"]["kdRatio"], 2)
                tdmscore = round(data["data"]["lifetime"]["mode"]["hc_hq"]["properties"]["score"])
                tdmspm = round(data["data"]["lifetime"]["mode"]["hc_hq"]["properties"]["scorePerMinute"], 2)
                tdmtime = round(data["data"]["lifetime"]["mode"]["hc_hq"]["properties"]["timePlayed"])
                embed.add_field(name="**Hardcore Headquarters Stats**", value=f"**Kills:** {hqkills} \n **Deaths:** {hqdeaths} \n **Kill/Death Ratio:** {hqkd} \n **Captures:** {hqcap} \n **Defends:** {hqdef} \n **Score:** {hqscore} \n **Score Per Minute:** {hqspm} \n **Time Played:** {hqtime}", inline=True)
            embeds.append(embed)
            #Kill Confirmed Stats
            embed = discord.Embed(title=userlvl + " - Kill Confirmed Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["mode"]["conf"]["properties"]["kills"] != "N/A":
                kckills = round(data["data"]["lifetime"]["mode"]["conf"]["properties"]["kills"])
                kcdeaths = round(data["data"]["lifetime"]["mode"]["conf"]["properties"]["deaths"])
                kccon = round(data["data"]["lifetime"]["mode"]["conf"]["properties"]["confirms"])
                kcden = round(data["data"]["lifetime"]["mode"]["conf"]["properties"]["denies"])
                kckd = round(data["data"]["lifetime"]["mode"]["conf"]["properties"]["kdRatio"], 2)
                kcscore = round(data["data"]["lifetime"]["mode"]["conf"]["properties"]["score"])
                kcspm = round(data["data"]["lifetime"]["mode"]["conf"]["properties"]["scorePerMinute"], 2)
                kctime = round(data["data"]["lifetime"]["mode"]["conf"]["properties"]["timePlayed"])
                embed.add_field(name="**Kill Confirmed Stats**", value=f"**Kills:** {kckills} \n **Deaths:** {kcdeaths} \n **Kill/Death Ratio:** {kckd} \n **Confirms:** {kccon} \n **Denies:** {kcden} \n **Score:** {kcscore} \n **Score Per Minute:** {kcspm} \n **Time Played:** {kctime}", inline=True)
            if data["data"]["lifetime"]["mode"]["hc_conf"]["properties"]["kills"] != "N/A":
                kckills = round(data["data"]["lifetime"]["mode"]["hc_conf"]["properties"]["kills"])
                kcdeaths = round(data["data"]["lifetime"]["mode"]["hc_conf"]["properties"]["deaths"])
                kccon = round(data["data"]["lifetime"]["mode"]["hc_conf"]["properties"]["confirms"])
                kcden = round(data["data"]["lifetime"]["mode"]["hc_conf"]["properties"]["denies"])
                kckd = round(data["data"]["lifetime"]["mode"]["hc_conf"]["properties"]["kdRatio"], 2)
                kcscore = round(data["data"]["lifetime"]["mode"]["hc_conf"]["properties"]["score"])
                kcspm = round(data["data"]["lifetime"]["mode"]["hc_conf"]["properties"]["scorePerMinute"], 2)
                kctime = round(data["data"]["lifetime"]["mode"]["hc_conf"]["properties"]["timePlayed"])
                embed.add_field(name="**Hardcore Kill Confirmed Stats**", value=f"**Kills:** {kckills} \n **Deaths:** {kcdeaths} \n **Kill/Death Ratio:** {kckd} \n **Confirms:** {kccon} \n **Denies:** {kcden} \n **Score:** {kcscore} \n **Score Per Minute:** {kcspm} \n **Time Played:** {kctime}", inline=True)
            embeds.append(embed)
            #Search and Destroy Stats
            embed = discord.Embed(title=userlvl + " - Search and Destroy Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["mode"]["sd"]["properties"]["kills"] != "N/A":
                sdkills = round(data["data"]["lifetime"]["mode"]["sd"]["properties"]["kills"])
                sddeaths = round(data["data"]["lifetime"]["mode"]["sd"]["properties"]["deaths"])
                sdplant = round(data["data"]["lifetime"]["mode"]["sd"]["properties"]["plants"])
                sddef = round(data["data"]["lifetime"]["mode"]["sd"]["properties"]["defuses"])
                sdkd = round(data["data"]["lifetime"]["mode"]["sd"]["properties"]["kdRatio"], 2)
                sdscore = round(data["data"]["lifetime"]["mode"]["sd"]["properties"]["score"])
                sdspm = round(data["data"]["lifetime"]["mode"]["sd"]["properties"]["scorePerMinute"], 2)
                sdtime = round(data["data"]["lifetime"]["mode"]["sd"]["properties"]["timePlayed"])
                embed.add_field(name="**Search and Destroy Stats**", value=f"**Kills:** {sdkills} \n **Deaths:** {sddeaths} \n **Kill/Death Ratio:** {sdkd} \n **Plants:** {sdplant} \n **Defuses:** {sddef} \n **Score:** {sdscore} \n **Score Per Minute:** {sdspm} \n **Time Played:** {sdtime}", inline=True)
            if data["data"]["lifetime"]["mode"]["hc_sd"]["properties"]["kills"] != "N/A":
                sdkills = round(data["data"]["lifetime"]["mode"]["hc_sd"]["properties"]["kills"])
                sddeaths = round(data["data"]["lifetime"]["mode"]["hc_sd"]["properties"]["deaths"])
                sdplant = round(data["data"]["lifetime"]["mode"]["hc_sd"]["properties"]["plants"])
                sddef = round(data["data"]["lifetime"]["mode"]["hc_sd"]["properties"]["defuses"])
                sdkd = round(data["data"]["lifetime"]["mode"]["hc_sd"]["properties"]["kdRatio"], 2)
                sdscore = round(data["data"]["lifetime"]["mode"]["hc_sd"]["properties"]["score"])
                sdspm = round(data["data"]["lifetime"]["mode"]["hc_sd"]["properties"]["scorePerMinute"], 2)
                sdtime = round(data["data"]["lifetime"]["mode"]["hc_sd"]["properties"]["timePlayed"])
                embed.add_field(name="**Hardcore Search and Destroy Stats**", value=f"**Kills:** {sdkills} \n **Deaths:** {sddeaths} \n **Kill/Death Ratio:** {sdkd} \n **Plants:** {sdplant} \n **Defuses:** {sddef} \n **Score:** {sdscore} \n **Score Per Minute:** {sdspm} \n **Time Played:** {sdtime}", inline=True)
            embeds.append(embed)
            #Cyber Attack Stats
            embed = discord.Embed(title=userlvl + " - Cyber Attack Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["mode"]["cyber"]["properties"]["kills"] != "N/A":
                cykills = round(data["data"]["lifetime"]["mode"]["cyber"]["properties"]["kills"])
                cydeaths = round(data["data"]["lifetime"]["mode"]["cyber"]["properties"]["deaths"])
                cyplant = round(data["data"]["lifetime"]["mode"]["cyber"]["properties"]["plants"])
                cyrev = round(data["data"]["lifetime"]["mode"]["cyber"]["properties"]["revives"])
                cykd = round(data["data"]["lifetime"]["mode"]["cyber"]["properties"]["kdRatio"], 2)
                cyscore = round(data["data"]["lifetime"]["mode"]["cyber"]["properties"]["score"])
                cyspm = round(data["data"]["lifetime"]["mode"]["cyber"]["properties"]["scorePerMinute"], 2)
                cytime = round(data["data"]["lifetime"]["mode"]["cyber"]["properties"]["timePlayed"])
                embed.add_field(name="**Cyber Attack Stats**", value=f"**Kills:** {cykills} \n **Deaths:** {cydeaths} \n **Kill/Death Ratio:** {cykd} \n **Plants:** {cyplant} \n **Revives:** {cyrev} \n **Score:** {cyscore} \n **Score Per Minute:** {cyspm} \n **Time Played:** {cytime}", inline=True)
            if data["data"]["lifetime"]["mode"]["hc_cyber"]["properties"]["kills"] != "N/A":
                cykills = round(data["data"]["lifetime"]["mode"]["hc_cyber"]["properties"]["kills"])
                cydeaths = round(data["data"]["lifetime"]["mode"]["hc_cyber"]["properties"]["deaths"])
                cyplant = round(data["data"]["lifetime"]["mode"]["hc_cyber"]["properties"]["plants"])
                cyrev = round(data["data"]["lifetime"]["mode"]["hc_cyber"]["properties"]["revives"])
                cykd = round(data["data"]["lifetime"]["mode"]["hc_cyber"]["properties"]["kdRatio"], 2)
                cyscore = round(data["data"]["lifetime"]["mode"]["hc_cyber"]["properties"]["score"])
                cyspm = round(data["data"]["lifetime"]["mode"]["hc_cyber"]["properties"]["scorePerMinute"], 2)
                cytime = round(data["data"]["lifetime"]["mode"]["hc_cyber"]["properties"]["timePlayed"])
                embed.add_field(name="**Hardcore Cyber Attack Stats**", value=f"**Kills:** {cykills} \n **Deaths:** {cydeaths} \n **Kill/Death Ratio:** {cykd} \n **Plants:** {cyplant} \n **Defuses:** {cyrev} \n **Score:** {cyscore} \n **Score Per Minute:** {cyspm} \n **Time Played:** {cytime}", inline=True)
            embeds.append(embed)
            #HardPoint Stats
            embed = discord.Embed(title=userlvl + " - HardPoint Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["mode"]["koth"]["properties"]["kills"] != "N/A":
                hpkills = round(data["data"]["lifetime"]["mode"]["koth"]["properties"]["kills"])
                hpdeaths = round(data["data"]["lifetime"]["mode"]["koth"]["properties"]["deaths"])
                hpobjtime = round(data["data"]["lifetime"]["mode"]["koth"]["properties"]["objTime"])
                hpdef = round(data["data"]["lifetime"]["mode"]["koth"]["properties"]["defends"])
                hpkd = round(data["data"]["lifetime"]["mode"]["koth"]["properties"]["kdRatio"], 2)
                hpscore = round(data["data"]["lifetime"]["mode"]["koth"]["properties"]["score"])
                hpspm = round(data["data"]["lifetime"]["mode"]["koth"]["properties"]["scorePerMinute"], 2)
                hptime = round(data["data"]["lifetime"]["mode"]["koth"]["properties"]["timePlayed"])
                embed.add_field(name="**HardPoint Stats**", value=f"**Kills:** {hpkills} \n **Deaths:** {hpdeaths} \n **Kill/Death Ratio:** {hpkd} \n **Objective Time:** {hpobjtime} \n **Defends:** {hpdef} \n **Score:** {hpscore} \n **Score Per Minute:** {hpspm} \n **Time Played:** {hptime}", inline=True)
            embeds.append(embed)
            #Weekly Stats
            embed = discord.Embed(title=userlvl + " - Weekly Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            try:
                if data["data"]["weekly"]["all"]["properties"]["medalXp"]:
                    kills = round(data["data"]["weekly"]["all"]["properties"]["kills"])
                    embed.add_field(name="**Kills**", value=f"**{kills}**", inline=True)
                    deaths = round(data["data"]["weekly"]["all"]["properties"]["deaths"])
                    embed.add_field(name="**Deaths**", value=f"**{deaths}**", inline=True)
                    assists = round(data["data"]["weekly"]["all"]["properties"]["assists"])
                    embed.add_field(name="**Assists**", value=f"**{assists}**", inline=True)
                    kd = round(data["data"]["weekly"]["all"]["properties"]["kdRatio"])
                    embed.add_field(name="**Kill/Death Ratio**", value=f"**{kd}**", inline=True)
                    wins = round(data["data"]["weekly"]["all"]["properties"]["wins"])
                    embed.add_field(name="**Wins**", value=f"**{wins}**", inline=True)
                    losses = round(data["data"]["weekly"]["all"]["properties"]["losses"])
                    embed.add_field(name="**Losses**", value=f"**{losses}**", inline=True)
                    winlo = round(data["data"]["weekly"]["all"]["properties"]["wlRatio"])
                    embed.add_field(name="**Win/Loss Ratio**", value=f"**{winlo}**", inline=True)
                    score = round(data["data"]["weekly"]["all"]["properties"]["score"])
                    embed.add_field(name="**Score**", value=f"**{score}**", inline=True)
                    spm = round(data["data"]["weekly"]["all"]["properties"]["scorePerMinute"], 2)
                    embed.add_field(name="**Score Per Minute**", value=f"**{spm}**", inline=True)
                    matches = round(data["data"]["weekly"]["all"]["properties"]["matchesPlayed"])
                    embed.add_field(name="**Matches Played**", value=f"**{matches}**", inline=True)
                    long = round(data["data"]["weekly"]["all"]["properties"]["longestStreak"])
                    embed.add_field(name="**Highest Killstreak**", value=f"**{long}**", inline=True)
                    headshots = round(data["data"]["weekly"]["all"]["properties"]["headshots"])
                    embed.add_field(name="**headshots**", value=f"**{headshots}**", inline=True)
                    time = round(data["data"]["weekly"]["all"]["properties"]["timePlayed"])
                    embed.add_field(name="**Time Played**", value=f"**{time}**", inline=True)
                embeds.append(embed)
            except:
                pass
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=180
            )
        except:
            await ctx.send("Either the platform or username is incorrect, please make sure to use pc, psn or xbox for the platform and make sure you spelt your name correctly.")
                                   
    @commands.command()
    async def codcareer(self, ctx, platform: Optional[str] = "", *, username: Optional[str] = ""):
        """Command to get your COD: MW career stats
        For platform use pc, xbox, psn"""
        embeds = []
        if platform + username == "":
            user = ctx.author
            platform = await self.conf.user(user).platform()
            username = await self.conf.user(user).username()
        username = username.replace(" ", "%20")
        username = username.replace("#", "%23")
        platform = platform.replace("pc", "battle")
        platform = platform.replace("xbox", "xbl")
        async with self._session.get(
                f"https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/{platform}/gamer/{username}/profile/type/mp"
            ) as request:
                data = await request.json()
        
        try:
            username = data["data"]["username"]
            level = round(data["data"]["level"])
            userlvl = f"{username} - Level: {level}"
            #Career Stats
            embed = discord.Embed(title=userlvl + " - Career Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            if data["data"]["lifetime"]["all"]["properties"]["totalShots"] != "N/A":
                totalshots = round(data["data"]["lifetime"]["all"]["properties"]["totalShots"])
                embed.add_field(name="**Total Shots**", value=totalshots, inline=True)
            if data["data"]["prestige"] != "N/A":
                prestige = round(data["data"]["prestige"])
                embed.add_field(name="**Prestige**", value=prestige, inline=True)
            if data["data"]["totalXp"] != "N/A":
                totalxp = round(data["data"]["totalXp"])
                embed.add_field(name="**Total XP**", value=totalxp, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["timePlayedTotal"] != "N/A":
                timeplayedtotal = round(data["data"]["lifetime"]["all"]["properties"]["timePlayedTotal"])
                embed.add_field(name="**Total Playtime**", value=timeplayedtotal, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["hits"] != "N/A":
                hits = round(data["data"]["lifetime"]["all"]["properties"]["hits"])
                embed.add_field(name="**Total Hits**", value=hits, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["score"] != "N/A":
                score = round(data["data"]["lifetime"]["all"]["properties"]["score"])
                embed.add_field(name="**Total Score**", value=score, inline=True)
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=180
            )
        except:
            await ctx.send("Either the platform or username is incorrect, please make sure to use pc, psn or xbox for the platform and make sure you spelt your name correctly.")

    @commands.command()
    async def codgame(self, ctx, platform: Optional[str] = "", *, username: Optional[str] = ""):
        """Command to get your COD: MW game stats
        For platform use pc, xbox, psn"""
        embeds = []
        if platform + username == "":
            user = ctx.author
            platform = await self.conf.user(user).platform()
            username = await self.conf.user(user).username()
        username = username.replace(" ", "%20")
        username = username.replace("#", "%23")
        platform = platform.replace("pc", "battle")
        platform = platform.replace("xbox", "xbl")
        async with self._session.get(
                f"https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/{platform}/gamer/{username}/profile/type/mp"
            ) as request:
                data = await request.json()
        
        try:
            username = data["data"]["username"]
            level = round(data["data"]["level"])
            userlvl = f"{username} - Level: {level}"
            #Game Stats
            embed = discord.Embed(title=userlvl + " - Game Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            if data["data"]["lifetime"]["all"]["properties"]["wins"] != "N/A":
                wins = round(data["data"]["lifetime"]["all"]["properties"]["wins"])
                embed.add_field(name="**Total Wins**", value=wins, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["losses"] != "N/A":
                losses = round(data["data"]["lifetime"]["all"]["properties"]["losses"])
                embed.add_field(name="**Total Losses**", value=losses, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["winLossRatio"] != "N/A":
                winloss = round(data["data"]["lifetime"]["all"]["properties"]["winLossRatio"], 2)
                embed.add_field(name="**Win/Loss Ratio**", value=winloss, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["gamesPlayed"] != "N/A":
                gamesplayed = round(data["data"]["lifetime"]["all"]["properties"]["gamesPlayed"])
                embed.add_field(name="**Total Games Played**", value=gamesplayed, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["kills"] != "N/A":
                kills = round(data["data"]["lifetime"]["all"]["properties"]["kills"])
                embed.add_field(name="**Total Kills**", value=kills, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["deaths"] != "N/A":
                deaths = round(data["data"]["lifetime"]["all"]["properties"]["deaths"])
                embed.add_field(name="**Total Deaths**", value=deaths, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["kdRatio"] != "N/A":
                killdeath = round(data["data"]["lifetime"]["all"]["properties"]["kdRatio"], 2)
                embed.add_field(name="**kill/Death Ratio**", value=killdeath, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["assists"] != "N/A":
                assists = round(data["data"]["lifetime"]["all"]["properties"]["assists"])
                embed.add_field(name="**Total Assists**", value=assists, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["headshots"] != "N/A":
                headshots = round(data["data"]["lifetime"]["all"]["properties"]["headshots"])
                embed.add_field(name="**Total headshots**", value=headshots, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["scorePerGame"] != "N/A":
                scoregame = round(data["data"]["lifetime"]["all"]["properties"]["scorePerGame"], 2)
                embed.add_field(name="**Score Per Game**", value=scoregame, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["bestKills"] != "N/A":
                bestkills = round(data["data"]["lifetime"]["all"]["properties"]["bestKills"])
                embed.add_field(name="**Highest Kills**", value=bestkills, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["currentWinStreak"] != "N/A":
                curwinstreak = round(data["data"]["lifetime"]["all"]["properties"]["currentWinStreak"])
                embed.add_field(name="**Current Win Streak**", value=curwinstreak, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["recordLongestWinStreak"] != "N/A":
                recwinstreak = round(data["data"]["lifetime"]["all"]["properties"]["recordLongestWinStreak"])
                embed.add_field(name="**Highest Win Streak**", value=recwinstreak, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["recordXpInAMatch"] != "N/A":
                recxp = round(data["data"]["lifetime"]["all"]["properties"]["recordXpInAMatch"])
                embed.add_field(name="**Highest Score**", value=recxp, inline=True)
            if data["data"]["lifetime"]["all"]["properties"]["recordKillStreak"] != "N/A":
                reckills = round(data["data"]["lifetime"]["all"]["properties"]["recordKillStreak"])
                embed.add_field(name="**Highest None Killsteak Kills**", value=reckills, inline=True)
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=180
            )
        except:
            await ctx.send("Either the platform or username is incorrect, please make sure to use pc, psn or xbox for the platform and make sure you spelt your name correctly.")

    @commands.command()
    async def codstreak(self, ctx, platform: Optional[str] = "", *, username: Optional[str] = ""):
        """Command to get your COD: MW killstreak stats
        For platform use pc, xbox, psn"""
        embeds = []
        if platform + username == "":
            user = ctx.author
            platform = await self.conf.user(user).platform()
            username = await self.conf.user(user).username()
        username = username.replace(" ", "%20")
        username = username.replace("#", "%23")
        platform = platform.replace("pc", "battle")
        platform = platform.replace("xbox", "xbl")
        async with self._session.get(
                f"https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/{platform}/gamer/{username}/profile/type/mp"
            ) as request:
                data = await request.json()
        
        try:
            username = data["data"]["username"]
            level = round(data["data"]["level"])
            userlvl = f"{username} - Level: {level}"
            #killstreak Stats
            embed = discord.Embed(title=userlvl + " - Killstreak Uses", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["radar_drone_overwatch"]["properties"]["uses"] != "N/A":
                radrov = round(data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["radar_drone_overwatch"]["properties"]["uses"])
                embed.add_field(name="**Personal Radar**", value=radrov, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["manual_turret"]["properties"]["uses"] != "N/A":
                mantur = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["manual_turret"]["properties"]["uses"])
                embed.add_field(name="**Shield Turret**", value=mantur, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["scrambler_drone_guard"]["properties"]["uses"] != "N/A":
                scdrgu = round(data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["scrambler_drone_guard"]["properties"]["uses"])
                embed.add_field(name="**Counter UAV**", value=scdrgu, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["uav"]["properties"]["uses"] != "N/A":
                uav = round(data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["uav"]["properties"]["uses"])
                embed.add_field(name="**UAV**", value=uav, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["airdrop"]["properties"]["uses"] != "N/A":
                airdro = round(data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["airdrop"]["properties"]["uses"])
                embed.add_field(name="**Care Package**", value=airdro, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["toma_strike"]["properties"]["uses"] != "N/A":
                tomstri = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["toma_strike"]["properties"]["uses"])
                embed.add_field(name="**Cluster Strike**", value=tomstri, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["cruise_predator"]["properties"]["uses"] != "N/A":
                crupred = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["cruise_predator"]["properties"]["uses"])
                embed.add_field(name="**Cruise Missile**", value=crupred, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["precision_airstrike"]["properties"]["uses"] != "N/A":
                precair = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["precision_airstrike"]["properties"]["uses"])
                embed.add_field(name="**Precision Airstrike**", value=precair, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["pac_sentry"]["properties"]["uses"] != "N/A":
                pacsen = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["pac_sentry"]["properties"]["uses"])
                embed.add_field(name="**Wheelson**", value=pacsen, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["bradley"]["properties"]["uses"] != "N/A":
                bradley = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["bradley"]["properties"]["uses"])
                embed.add_field(name="**Infantry Vehicle**", value=bradley, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["sentry_gun"]["properties"]["uses"] != "N/A":
                sengun = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["sentry_gun"]["properties"]["uses"])
                embed.add_field(name="**Sentry Gun**", value=sengun, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["airdrop_multiple"]["properties"]["uses"] != "N/A":
                airmult = round(data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["airdrop_multiple"]["properties"]["uses"])
                embed.add_field(name="**Emergency Airdrop**", value=airmult, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["hover_jet"]["properties"]["uses"] != "N/A":
                hovjet = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["hover_jet"]["properties"]["uses"])
                embed.add_field(name="**VTOL Jet**", value=hovjet, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["chopper_gunner"]["properties"]["uses"] != "N/A":
                chopgun = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["chopper_gunner"]["properties"]["uses"])
                embed.add_field(name="**Chopper Gunner**", value=chopgun, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["white_phosphorus"]["properties"]["uses"] != "N/A":
                whipho = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["white_phosphorus"]["properties"]["uses"])
                embed.add_field(name="**White Phosphorus**", value=whipho, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["chopper_support"]["properties"]["uses"] != "N/A":
                chopsup = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["chopper_support"]["properties"]["uses"])
                embed.add_field(name="**Support Helo**", value=chopsup, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["gunship"]["properties"]["uses"] != "N/A":
                gunship = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["gunship"]["properties"]["uses"])
                embed.add_field(name="**Gunship**", value=gunship, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["directional_uav"]["properties"]["uses"] != "N/A":
                diruav = round(data["data"]["lifetime"]["scorestreakData"]["supportScorestreakData"]["directional_uav"]["properties"]["uses"])
                embed.add_field(name="**Advanced UAV**", value=diruav, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["juggernaut"]["properties"]["uses"] != "N/A":
                jugger = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["juggernaut"]["properties"]["uses"])
                embed.add_field(name="**Juggernaut**", value=jugger, inline=True)
            if data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["nuke"]["properties"]["uses"] != "N/A":
                nuke = round(data["data"]["lifetime"]["scorestreakData"]["lethalScorestreakData"]["nuke"]["properties"]["uses"])
                embed.add_field(name="**Nuke**", value=nuke, inline=True)
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=180
            )
        except:
            await ctx.send("Either the platform or username is incorrect, please make sure to use pc, psn or xbox for the platform and make sure you spelt your name correctly.")

    @commands.command()
    async def codassault(self, ctx, platform: Optional[str] = "", *, username: Optional[str] = ""):
        """Command to get your COD: MW assault rifle stats
        For platform use pc, xbox, psn"""
        embeds = []
        if platform + username == "":
            user = ctx.author
            platform = await self.conf.user(user).platform()
            username = await self.conf.user(user).username()
        username = username.replace(" ", "%20")
        username = username.replace("#", "%23")
        platform = platform.replace("pc", "battle")
        platform = platform.replace("xbox", "xbl")
        async with self._session.get(
                f"https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/{platform}/gamer/{username}/profile/type/mp"
            ) as request:
                data = await request.json()
        
        try:
            username = data["data"]["username"]
            level = round(data["data"]["level"])
            userlvl = f"{username} - Level: {level}"
            #Assault Rifle Stats
            embed = discord.Embed(title=userlvl + " - Assault Rifle Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_kilo433"]["properties"]["kills"] != "N/A":
                kilo = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_kilo433"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_kilo433"]["properties"]["headshots"])
                embed.add_field(name="**Kilo 141 Stats**", value=f"**Kills:** {kilo} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_mike4"]["properties"]["kills"] != "N/A":
                m4a1 = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_mike4"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_mike4"]["properties"]["headshots"])
                embed.add_field(name="**M4A1 Stats**", value=f"**Kills:** {m4a1} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_falpha"]["properties"]["kills"] != "N/A":
                FR = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_falpha"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_falpha"]["properties"]["headshots"])
                embed.add_field(name="**FR 5.56 Stats**", value=f"**Kills:** {FR} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_asierra12"]["properties"]["kills"] != "N/A":
                oden = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_asierra12"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_asierra12"]["properties"]["headshots"])
                embed.add_field(name="**Oden Stats**", value=f"**Kills:** {oden} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_akilo47"]["properties"]["kills"] != "N/A":
                ak = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_akilo47"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_akilo47"]["properties"]["headshots"])
                embed.add_field(name="**AK-47 Stats**", value=f"**Kills:** {ak} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_scharlie"]["properties"]["kills"] != "N/A":
                scar = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_scharlie"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_scharlie"]["properties"]["headshots"])
                embed.add_field(name="**FN Scar 17 Stats**", value=f"**Kills:** {scar} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_falima"]["properties"]["kills"] != "N/A":
                fal = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_falima"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_falima"]["properties"]["headshots"])
                embed.add_field(name="**FAL Stats**", value=f"**Kills:** {fal} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_mcharlie"]["properties"]["kills"] != "N/A":
                m13 = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_mcharlie"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_mcharlie"]["properties"]["headshots"])
                embed.add_field(name="**M13 Stats**", value=f"**Kills:** {m13} \n **headshots:** {headshots}", inline=True)
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=180
            )
        except:
            await ctx.send("Either the platform or username is incorrect, please make sure to use pc, psn or xbox for the platform and make sure you spelt your name correctly.")

    @commands.command()
    async def codlmg(self, ctx, platform: Optional[str] = "", *, username: Optional[str] = ""):
        """Command to get your COD: MW LMG stats
        For platform use pc, xbox, psn"""
        embeds = []
        if platform + username == "":
            user = ctx.author
            platform = await self.conf.user(user).platform()
            username = await self.conf.user(user).username()
        username = username.replace(" ", "%20")
        username = username.replace("#", "%23")
        platform = platform.replace("pc", "battle")
        platform = platform.replace("xbox", "xbl")
        async with self._session.get(
                f"https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/{platform}/gamer/{username}/profile/type/mp"
            ) as request:
                data = await request.json()
        try:
            username = data["data"]["username"]
            level = round(data["data"]["level"])
            userlvl = f"{username} - Level: {level}"
            #LMG Stats
            embed = discord.Embed(title=userlvl + " - LMG Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_kilo121"]["properties"]["kills"] != "N/A":
                m91 = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_kilo121"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_kilo121"]["properties"]["headshots"])
                embed.add_field(name="**M91 Stats**", value=f"**Kills:** {m91} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_lima86"]["properties"]["kills"] != "N/A":
                sa87 = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_lima86"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_lima86"]["properties"]["headshots"])
                embed.add_field(name="**SA87 Stats**", value=f"**Kills:** {sa87} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_mgolf34"]["properties"]["kills"] != "N/A":
                mg34 = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_mgolf34"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_mgolf34"]["properties"]["headshots"])
                embed.add_field(name="**MG34 Stats**", value=f"**Kills:** {mg34} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_pkilo"]["properties"]["kills"] != "N/A":
                pkm = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_pkilo"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_pkilo"]["properties"]["headshots"])
                embed.add_field(name="**PKM Stats**", value=f"**Kills:** {pkm} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_mgolf36"]["properties"]["kills"] != "N/A":
                holger = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_mgolf36"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_mgolf36"]["properties"]["headshots"])
                embed.add_field(name="**Holger-26 Stats**", value=f"**Kills:** {holger} \n **headshots:** {headshots}", inline=True)
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=180
            )
        except:
            await ctx.send("Either the platform or username is incorrect, please make sure to use pc, psn or xbox for the platform and make sure you spelt your name correctly.")

    @commands.command()
    async def codlaunch(self, ctx, platform: Optional[str] = "", *, username: Optional[str] = ""):
        """Command to get your COD: MW launcher stats
        For platform use pc, xbox, psn"""
        embeds = []
        if platform + username == "":
            user = ctx.author
            platform = await self.conf.user(user).platform()
            username = await self.conf.user(user).username()
        username = username.replace(" ", "%20")
        username = username.replace("#", "%23")
        platform = platform.replace("pc", "battle")
        platform = platform.replace("xbox", "xbl")
        async with self._session.get(
                f"https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/{platform}/gamer/{username}/profile/type/mp"
            ) as request:
                data = await request.json()
        
        try:
            username = data["data"]["username"]
            level = round(data["data"]["level"])
            userlvl = f"{username} - Level: {level}"
            #Launcher Stats
            embed = discord.Embed(title=userlvl + " - Launcher Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_gromeo"]["properties"]["kills"] != "N/A":
                pila = round(data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_gromeo"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_gromeo"]["properties"]["headshots"])
                embed.add_field(name="**PILA Stats**", value=f"**Kills:** {pila} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_rpapa7"]["properties"]["kills"] != "N/A":
                rpg = round(data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_rpapa7"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_rpapa7"]["properties"]["headshots"])
                embed.add_field(name="**RPG-7 Stats**", value=f"**Kills:** {rpg} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_juliet"]["properties"]["kills"] != "N/A":
                jokr = round(data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_juliet"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_juliet"]["properties"]["headshots"])
                embed.add_field(name="**JOKR Stats**", value=f"**Kills:** {jokr} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_kgolf"]["properties"]["kills"] != "N/A":
                strella = round(data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_kgolf"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_kgolf"]["properties"]["headshots"])
                embed.add_field(name="**Strella-P Stats**", value=f"**Kills:** {strella} \n **headshots:** {headshots}", inline=True)
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=180
            )
        except:
            await ctx.send("Either the platform or username is incorrect, please make sure to use pc, psn or xbox for the platform and make sure you spelt your name correctly.")

    @commands.command()
    async def codpistol(self, ctx, platform: Optional[str] = "", *, username: Optional[str] = ""):
        """Command to get your COD: MW pistol stats
        For platform use pc, xbox, psn"""
        embeds = []
        if platform + username == "":
            user = ctx.author
            platform = await self.conf.user(user).platform()
            username = await self.conf.user(user).username()
        username = username.replace(" ", "%20")
        username = username.replace("#", "%23")
        platform = platform.replace("pc", "battle")
        platform = platform.replace("xbox", "xbl")
        async with self._session.get(
                f"https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/{platform}/gamer/{username}/profile/type/mp"
            ) as request:
                data = await request.json()
        
        try:
            username = data["data"]["username"]
            level = round(data["data"]["level"])
            userlvl = f"{username} - Level: {level}"
            #Pistol Stats
            embed = discord.Embed(title=userlvl + " - Pistol Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_decho"]["properties"]["kills"] != "N/A":
                gs = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_decho"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_decho"]["properties"]["headshots"])
                embed.add_field(name="**.50 GS Stats**", value=f"**Kills:** {gs} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_cpapa"]["properties"]["kills"] != "N/A":
                revol = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_cpapa"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_cpapa"]["properties"]["headshots"])
                embed.add_field(name="**.357 Stats**", value=f"**Kills:** {revol} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_mike1911"]["properties"]["kills"] != "N/A":
                m1911 = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_mike1911"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_mike1911"]["properties"]["headshots"])
                embed.add_field(name="**1911 Stats**", value=f"**Kills:** {m1911} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_golf21"]["properties"]["kills"] != "N/A":
                x16 = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_golf21"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_golf21"]["properties"]["headshots"])
                embed.add_field(name="**X16 Stats**", value=f"**Kills:** {x16} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_papa320"]["properties"]["kills"] != "N/A":
                m19 = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_papa320"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_papa320"]["properties"]["headshots"])
                embed.add_field(name="**M19 Stats**", value=f"**Kills:** {m19} \n **headshots:** {headshots}", inline=True)
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=180
            )
        except:
            await ctx.send("Either the platform or username is incorrect, please make sure to use pc, psn or xbox for the platform and make sure you spelt your name correctly.")

    @commands.command()
    async def codshotgun(self, ctx, platform: Optional[str] = "", *, username: Optional[str] = ""):
        """Command to get your COD: MW shotgun stats
        For platform use pc, xbox, psn"""
        embeds = []
        if platform + username == "":
            user = ctx.author
            platform = await self.conf.user(user).platform()
            username = await self.conf.user(user).username()
        username = username.replace(" ", "%20")
        username = username.replace("#", "%23")
        platform = platform.replace("pc", "battle")
        platform = platform.replace("xbox", "xbl")
        async with self._session.get(
                f"https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/{platform}/gamer/{username}/profile/type/mp"
            ) as request:
                data = await request.json()
        
        try:
            username = data["data"]["username"]
            level = round(data["data"]["level"])
            userlvl = f"{username} - Level: {level}"
            #Shotgun Stats
            embed = discord.Embed(title=userlvl + " - Shotgun Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_charlie725"]["properties"]["kills"] != "N/A":
                farmer = round(data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_charlie725"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_charlie725"]["properties"]["headshots"])
                embed.add_field(name="**725 Stats**", value=f"**Kills:** {farmer} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_romeo870"]["properties"]["kills"] != "N/A":
                model = round(data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_romeo870"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_romeo870"]["properties"]["headshots"])
                embed.add_field(name="**Model 680 Stats**", value=f"**Kills:** {model} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_oscar12"]["properties"]["kills"] != "N/A":
                origin = round(data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_oscar12"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_oscar12"]["properties"]["headshots"])
                embed.add_field(name="**Origin 12 Shotgun Stats**", value=f"**Kills:** {origin} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_dpapa12"]["properties"]["kills"] != "N/A":
                r9 = round(data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_dpapa12"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_dpapa12"]["properties"]["headshots"])
                embed.add_field(name="**R9-0 Shotgun Stats**", value=f"**Kills:** {r9} \n **headshots:** {headshots}", inline=True)
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=180
            )
        except:
            await ctx.send("Either the platform or username is incorrect, please make sure to use pc, psn or xbox for the platform and make sure you spelt your name correctly.")

    @commands.command()
    async def codsmg(self, ctx, platform: Optional[str] = "", *, username: Optional[str] = ""):
        """Command to get your COD: MW SMG stats
        For platform use pc, xbox, psn"""
        embeds = []
        if platform + username == "":
            user = ctx.author
            platform = await self.conf.user(user).platform()
            username = await self.conf.user(user).username()
        username = username.replace(" ", "%20")
        username = username.replace("#", "%23")
        platform = platform.replace("pc", "battle")
        platform = platform.replace("xbox", "xbl")
        async with self._session.get(
                f"https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/{platform}/gamer/{username}/profile/type/mp"
            ) as request:
                data = await request.json()
        try:
            username = data["data"]["username"]
            level = round(data["data"]["level"])
            userlvl = f"{username} - Level: {level}"
            #SMG Stats
            embed = discord.Embed(title=userlvl + " - SMG Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_mpapa7"]["properties"]["kills"] != "N/A":
                mp7 = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_mpapa7"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_mpapa7"]["properties"]["headshots"])
                embed.add_field(name="**MP7 Stats**", value=f"**Kills:** {mp7} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_augolf"]["properties"]["kills"] != "N/A":
                aug = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_augolf"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_augolf"]["properties"]["headshots"])
                embed.add_field(name="**AUG Stats**", value=f"**Kills:** {aug} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_papa90"]["properties"]["kills"] != "N/A":
                p90 = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_papa90"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_papa90"]["properties"]["headshots"])
                embed.add_field(name="**P90 Stats**", value=f"**Kills:** {p90} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_mpapa5"]["properties"]["kills"] != "N/A":
                mp5 = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_mpapa5"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_mpapa5"]["properties"]["headshots"])
                embed.add_field(name="**MP5 Stats**", value=f"**Kills:** {mp5} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_beta"]["properties"]["kills"] != "N/A":
                bizon = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_beta"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_beta"]["properties"]["headshots"])
                embed.add_field(name="**PP19 Bizon Stats**", value=f"**Kills:** {bizon} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_uzulu"]["properties"]["kills"] != "N/A":
                uzi = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_uzulu"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_uzulu"]["properties"]["headshots"])
                embed.add_field(name="**Uzi Stats**", value=f"**Kills:** {uzi} \n **headshots:** {headshots}", inline=True)
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=180
            )
        except:
            await ctx.send("Either the platform or username is incorrect, please make sure to use pc, psn or xbox for the platform and make sure you spelt your name correctly.")

    @commands.command()
    async def codsniper(self, ctx, platform: Optional[str] = "", *, username: Optional[str] = ""):
        """Command to get your COD: MW sniper stats
        For platform use pc, xbox, psn"""
        embeds = []
        if platform + username == "":
            user = ctx.author
            platform = await self.conf.user(user).platform()
            username = await self.conf.user(user).username()
        username = username.replace(" ", "%20")
        username = username.replace("#", "%23")
        platform = platform.replace("pc", "battle")
        platform = platform.replace("xbox", "xbl")
        async with self._session.get(
                f"https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/{platform}/gamer/{username}/profile/type/mp"
            ) as request:
                data = await request.json()
        try:
            username = data["data"]["username"]
            level = round(data["data"]["level"])
            userlvl = f"{username} - Level: {level}"
            #Sniper Rifle Stats
            embed = discord.Embed(title=userlvl + " - Sniper Rifle Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["weapon_sniper"]["iw8_sn_hdromeo"]["properties"]["kills"] != "N/A":
                hdr = round(data["data"]["lifetime"]["itemData"]["weapon_sniper"]["iw8_sn_hdromeo"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_sniper"]["iw8_sn_hdromeo"]["properties"]["headshots"])
                embed.add_field(name="**HDR Stats**", value=f"**Kills:** {hdr} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_sniper"]["iw8_sn_alpha50"]["properties"]["kills"] != "N/A":
                ax = round(data["data"]["lifetime"]["itemData"]["weapon_sniper"]["iw8_sn_alpha50"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_sniper"]["iw8_sn_alpha50"]["properties"]["headshots"])
                embed.add_field(name="**AX-50 Stats**", value=f"**Kills:** {ax} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_sniper"]["iw8_sn_delta"]["properties"]["kills"] != "N/A":
                drag = round(data["data"]["lifetime"]["itemData"]["weapon_sniper"]["iw8_sn_delta"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_marksman"]["iw8_sn_delta"]["properties"]["headshots"])
                embed.add_field(name="**Dragunov Stats**", value=f"**Kills:** {drag} \n **headshots:** {headshots}", inline=True)
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=180
            )
        except:
            await ctx.send("Either the platform or username is incorrect, please make sure to use pc, psn or xbox for the platform and make sure you spelt your name correctly.")
    @commands.command()
    async def codmarksman(self, ctx, platform: Optional[str] = "", *, username: Optional[str] = ""):
        """Command to get your COD: MW marksman rifle stats
        For platform use pc, xbox, psn"""
        embeds = []
        if platform + username == "":
            user = ctx.author
            platform = await self.conf.user(user).platform()
            username = await self.conf.user(user).username()
        username = username.replace(" ", "%20")
        username = username.replace("#", "%23")
        platform = platform.replace("pc", "battle")
        platform = platform.replace("xbox", "xbl")
        async with self._session.get(
                f"https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/{platform}/gamer/{username}/profile/type/mp"
            ) as request:
                data = await request.json()

        try:
            username = data["data"]["username"]
            level = round(data["data"]["level"])
            userlvl = f"{username} - Level: {level}"
           #Marksman Rifle Stats
            embed = discord.Embed(title=userlvl + " - Marksman Rifle Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["weapon_marksman"]["iw8_sn_kilo98"]["properties"]["kills"] != "N/A":
                kar = round(data["data"]["lifetime"]["itemData"]["weapon_marksman"]["iw8_sn_kilo98"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_marksman"]["iw8_sn_kilo98"]["properties"]["headshots"])
                embed.add_field(name="**Kar98K Stats**", value=f"**Kills:** {kar} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_marksman"]["iw8_sn_sbeta"]["properties"]["kills"] != "N/A":
                carbine = round(data["data"]["lifetime"]["itemData"]["weapon_marksman"]["iw8_sn_sbeta"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_marksman"]["iw8_sn_sbeta"]["properties"]["headshots"])
                embed.add_field(name="**MK2 Carbine Stats**", value=f"**Kills:** {carbine} \n **headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_marksman"]["iw8_sn_mike14"]["properties"]["kills"] != "N/A":
                ebr = round(data["data"]["lifetime"]["itemData"]["weapon_marksman"]["iw8_sn_mike14"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_marksman"]["iw8_sn_mike14"]["properties"]["headshots"])
                embed.add_field(name="**EBR-14 Stats**", value=f"**Kills:** {ebr} \n **headshots:** {headshots}", inline=True)
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=180
            )
        except:
            await ctx.send("Either the platform or username is incorrect, please make sure to use pc, psn or xbox for the platform and make sure you spelt your name correctly.")

    @commands.command()
    async def codmelee(self, ctx, platform: Optional[str] = "", *, username: Optional[str] = ""):
        """Command to get your COD: MW melee stats
        For platform use pc, xbox, psn"""
        embeds = []
        if platform + username == "":
            user = ctx.author
            platform = await self.conf.user(user).platform()
            username = await self.conf.user(user).username()
        username = username.replace(" ", "%20")
        username = username.replace("#", "%23")
        platform = platform.replace("pc", "battle")
        platform = platform.replace("xbox", "xbl")
        async with self._session.get(
                f"https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/{platform}/gamer/{username}/profile/type/mp"
            ) as request:
                data = await request.json()
        
        try:
            username = data["data"]["username"]
            level = round(data["data"]["level"])
            userlvl = f"{username} - Level: {level}"
            #Melee Stats
            embed = discord.Embed(title=userlvl + " - Melee Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["weapon_other"]["iw8_me_riotshield"]["properties"]["hits"] != "N/A":
                riothit = round(data["data"]["lifetime"]["itemData"]["weapon_other"]["iw8_me_riotshield"]["properties"]["hits"])
                riotkill = round(data["data"]["lifetime"]["itemData"]["weapon_other"]["iw8_me_riotshield"]["properties"]["kills"])
                riotob = round(data["data"]["lifetime"]["accoladeData"]["properties"]["riotShieldDamageAbsorbed"])
                embed.add_field(name="**Riotshield Stats**", value=f"**Hits:** {riothit} \n **Kills:** {riotkill} \n **Damage Obsorbed:** {riotob}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_melee"]["iw8_knife"]["properties"]["kills"] != "N/A":
                knifekill = round(data["data"]["lifetime"]["itemData"]["weapon_melee"]["iw8_knife"]["properties"]["kills"])
                embed.add_field(name="**Combat Knife Stats**", value=f"**Kills:** {knifekill}", inline=True)
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=180
            )
        except:
            await ctx.send("Either the platform or username is incorrect, please make sure to use pc, psn or xbox for the platform and make sure you spelt your name correctly.")

    @commands.command()
    async def codgrenade(self, ctx, platform: Optional[str] = "", *, username: Optional[str] = ""):
        """Command to get your COD: MW grenade stats
        For platform use pc, xbox, psn"""
        embeds = []
        if platform + username == "":
            user = ctx.author
            platform = await self.conf.user(user).platform()
            username = await self.conf.user(user).username()
        username = username.replace(" ", "%20")
        username = username.replace("#", "%23")
        platform = platform.replace("pc", "battle")
        platform = platform.replace("xbox", "xbl")
        async with self._session.get(
                f"https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/{platform}/gamer/{username}/profile/type/mp"
            ) as request:
                data = await request.json()
        
        try:
            username = data["data"]["username"]
            level = round(data["data"]["level"])
            userlvl = f"{username} - Level: {level}"
            #Grenade Stats
            embed = discord.Embed(title=userlvl + " - Grenade Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["lethals"]["equip_frag"]["properties"]["kills"] != "N/A":
                frag = round(data["data"]["lifetime"]["itemData"]["lethals"]["equip_frag"]["properties"]["kills"])
                embed.add_field(name="**Frag Grenade Stats**", value=f"**Kills:** {frag}", inline=True)
            if data["data"]["lifetime"]["itemData"]["lethals"]["equip_thermite"]["properties"]["kills"] != "N/A":
                thermite = round(data["data"]["lifetime"]["itemData"]["lethals"]["equip_thermite"]["properties"]["kills"])
                embed.add_field(name="**Thermite Grenade Stats**", value=f"**Kills:** {thermite}", inline=True)
            if data["data"]["lifetime"]["itemData"]["lethals"]["equip_semtex"]["properties"]["kills"] != "N/A":
                semtex = round(data["data"]["lifetime"]["itemData"]["lethals"]["equip_semtex"]["properties"]["kills"])
                embed.add_field(name="**Semtex Grenade Stats**", value=f"**Kills:** {semtex}", inline=True)
            if data["data"]["lifetime"]["itemData"]["lethals"]["equip_claymore"]["properties"]["kills"] != "N/A":
                claymore = round(data["data"]["lifetime"]["itemData"]["lethals"]["equip_claymore"]["properties"]["kills"])
                embed.add_field(name="**Claymore Stats**", value=f"**Kills:** {claymore}", inline=True)
            if data["data"]["lifetime"]["itemData"]["lethals"]["equip_c4"]["properties"]["kills"] != "N/A":
                c4 = round(data["data"]["lifetime"]["itemData"]["lethals"]["equip_c4"]["properties"]["kills"])
                embed.add_field(name="**C4 Stats**", value=f"**Kills:** {c4}", inline=True)
            if data["data"]["lifetime"]["itemData"]["lethals"]["equip_at_mine"]["properties"]["kills"] != "N/A":
                atmine = round(data["data"]["lifetime"]["itemData"]["lethals"]["equip_at_mine"]["properties"]["kills"])
                embed.add_field(name="**Anti-Tank Mine Stats**", value=f"**Kills:** {atmine}", inline=True)
            if data["data"]["lifetime"]["itemData"]["lethals"]["equip_throwing_knife"]["properties"]["kills"] != "N/A":
                throw = round(data["data"]["lifetime"]["itemData"]["lethals"]["equip_throwing_knife"]["properties"]["kills"])
                embed.add_field(name="**Throwing Knife Stats**", value=f"**Kills:** {throw}", inline=True)
            if data["data"]["lifetime"]["itemData"]["lethals"]["equip_molotov"]["properties"]["kills"] != "N/A":
                molotov = round(data["data"]["lifetime"]["itemData"]["lethals"]["equip_molotov"]["properties"]["kills"])
                embed.add_field(name="**Molotov Stats**", value=f"**Kills:** {molotov}", inline=True)
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=180
            )
        except:
            await ctx.send("Either the platform or username is incorrect, please make sure to use pc, psn or xbox for the platform and make sure you spelt your name correctly.")

    @commands.command()
    async def coddom(self, ctx, platform: Optional[str] = "", *, username: Optional[str] = ""):
        """Command to get your COD: MW domination stats
        For platform use pc, xbox, psn"""
        embeds = []
        if platform + username == "":
            user = ctx.author
            platform = await self.conf.user(user).platform()
            username = await self.conf.user(user).username()
        username = username.replace(" ", "%20")
        username = username.replace("#", "%23")
        platform = platform.replace("pc", "battle")
        platform = platform.replace("xbox", "xbl")
        async with self._session.get(
                f"https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/{platform}/gamer/{username}/profile/type/mp"
            ) as request:
                data = await request.json()
        
        try:
            username = data["data"]["username"]
            level = round(data["data"]["level"])
            userlvl = f"{username} - Level: {level}"
            #Domination Stats
            embed = discord.Embed(title=userlvl + " - Domination Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["mode"]["dom"]["properties"]["kills"] != "N/A":
                domkills = round(data["data"]["lifetime"]["mode"]["dom"]["properties"]["kills"])
                domdeaths = round(data["data"]["lifetime"]["mode"]["dom"]["properties"]["deaths"])
                domkd = round(data["data"]["lifetime"]["mode"]["dom"]["properties"]["kdRatio"], 2)
                domscore = round(data["data"]["lifetime"]["mode"]["dom"]["properties"]["score"])
                domcapture = round(data["data"]["lifetime"]["mode"]["dom"]["properties"]["captures"])
                domdef = round(data["data"]["lifetime"]["mode"]["dom"]["properties"]["defends"])
                domscore = round(data["data"]["lifetime"]["mode"]["dom"]["properties"]["score"])
                domspm = round(data["data"]["lifetime"]["mode"]["dom"]["properties"]["scorePerMinute"])
                domtime = round(data["data"]["lifetime"]["mode"]["dom"]["properties"]["timePlayed"])
                embed.add_field(name="**Domination Stats**", value=f"**Kills:** {domkills} \n **Deaths:** {domdeaths} \n **Kill/Death Ratio:** {domkd} \n **Captures:** {domcapture} \n **Defends:** {domdef} \n **Score:** {domscore} \n **Score Per Minute:** {domspm} \n **Time Played:** {domtime}", inline=True)
            if data["data"]["lifetime"]["mode"]["hc_dom"]["properties"]["kills"] != "N/A":
                domkills = round(data["data"]["lifetime"]["mode"]["hc_dom"]["properties"]["kills"])
                domdeaths = round(data["data"]["lifetime"]["mode"]["hc_dom"]["properties"]["deaths"])
                domkd = round(data["data"]["lifetime"]["mode"]["hc_dom"]["properties"]["kdRatio"], 2)
                domscore = round(data["data"]["lifetime"]["mode"]["hc_dom"]["properties"]["score"])
                domcapture = round(data["data"]["lifetime"]["mode"]["hc_dom"]["properties"]["captures"])
                domdef = round(data["data"]["lifetime"]["mode"]["hc_dom"]["properties"]["defends"])
                domscore = round(data["data"]["lifetime"]["mode"]["hc_dom"]["properties"]["score"])
                domspm = round(data["data"]["lifetime"]["mode"]["hc_dom"]["properties"]["scorePerMinute"])
                domtime = round(data["data"]["lifetime"]["mode"]["hc_dom"]["properties"]["timePlayed"])
                embed.add_field(name="**Hardcore Domination Stats**", value=f"**Kills:** {domkills} \n **Deaths:** {domdeaths} \n **Kill/Death Ratio:** {domkd} \n **Captures:** {domcapture} \n **Defends:** {domdef} \n **Score:** {domscore} \n **Score Per Minute:** {domspm} \n **Time Played:** {domtime}", inline=True)
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=180
            )
        except:
            await ctx.send("Either the platform or username is incorrect, please make sure to use pc, psn or xbox for the platform and make sure you spelt your name correctly.")

    @commands.command()
    async def codtdm(self, ctx, platform: Optional[str] = "", *, username: Optional[str] = ""):
        """Command to get your COD: MW team deathmatch stats
        For platform use pc, xbox, psn"""
        embeds = []
        if platform + username == "":
            user = ctx.author
            platform = await self.conf.user(user).platform()
            username = await self.conf.user(user).username()
        username = username.replace(" ", "%20")
        username = username.replace("#", "%23")
        platform = platform.replace("pc", "battle")
        platform = platform.replace("xbox", "xbl")
        async with self._session.get(
                f"https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/{platform}/gamer/{username}/profile/type/mp"
            ) as request:
                data = await request.json()
        
        try:
            username = data["data"]["username"]
            level = round(data["data"]["level"])
            userlvl = f"{username} - Level: {level}"
            #TeamDeathMatch Stats
            embed = discord.Embed(title=userlvl + " - Team Deathmatch Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["mode"]["war"]["properties"]["kills"] != "N/A":
                tdmkills = round(data["data"]["lifetime"]["mode"]["war"]["properties"]["kills"])
                tdmdeaths = round(data["data"]["lifetime"]["mode"]["war"]["properties"]["deaths"])
                tdmassists = round(data["data"]["lifetime"]["mode"]["war"]["properties"]["assists"])
                tdmkd = round(data["data"]["lifetime"]["mode"]["war"]["properties"]["kdRatio"], 2)
                tdmscore = round(data["data"]["lifetime"]["mode"]["war"]["properties"]["score"])
                tdmspm = round(data["data"]["lifetime"]["mode"]["war"]["properties"]["scorePerMinute"], 2)
                tdmtime = round(data["data"]["lifetime"]["mode"]["war"]["properties"]["timePlayed"])
                embed.add_field(name="**Team Deathmatch Stats**", value=f"**Kills:** {tdmkills} \n **Deaths:** {tdmdeaths} \n **Assists:** {tdmassists} \n **Kill/Death Ratio:** {tdmkd} \n **Score:** {tdmscore} \n **Score Per Minute:** {tdmspm} \n **Time Played:** {tdmtime}", inline=True)
            if data["data"]["lifetime"]["mode"]["hc_war"]["properties"]["kills"] != "N/A":
                tdmkills = round(data["data"]["lifetime"]["mode"]["hc_war"]["properties"]["kills"])
                tdmdeaths = round(data["data"]["lifetime"]["mode"]["hc_war"]["properties"]["deaths"])
                tdmassists = round(data["data"]["lifetime"]["mode"]["hc_war"]["properties"]["assists"])
                tdmkd = round(data["data"]["lifetime"]["mode"]["hc_war"]["properties"]["kdRatio"], 2)
                tdmscore = round(data["data"]["lifetime"]["mode"]["hc_war"]["properties"]["score"])
                tdmspm = round(data["data"]["lifetime"]["mode"]["hc_war"]["properties"]["scorePerMinute"], 2)
                tdmtime = round(data["data"]["lifetime"]["mode"]["hc_war"]["properties"]["timePlayed"])
                embed.add_field(name="**Hardcore Team Deathmatch Stats**", value=f"**Kills:** {tdmkills} \n **Deaths:** {tdmdeaths} \n **Assists:** {tdmassists} \n **Kill/Death Ratio:** {tdmkd} \n **Score:** {tdmscore} \n **Score Per Minute:** {tdmspm} \n **Time Played:** {tdmtime}", inline=True)
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=180
            )
        except:
            await ctx.send("Either the platform or username is incorrect, please make sure to use pc, psn or xbox for the platform and make sure you spelt your name correctly.")

    @commands.command()
    async def codhq(self, ctx, platform: Optional[str] = "", *, username: Optional[str] = ""):
        """Command to get your COD: MW headquarters stats
        For platform use pc, xbox, psn"""
        embeds = []
        if platform + username == "":
            user = ctx.author
            platform = await self.conf.user(user).platform()
            username = await self.conf.user(user).username()
        username = username.replace(" ", "%20")
        username = username.replace("#", "%23")
        platform = platform.replace("pc", "battle")
        platform = platform.replace("xbox", "xbl")
        async with self._session.get(
                f"https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/{platform}/gamer/{username}/profile/type/mp"
            ) as request:
                data = await request.json()
        
        try:
            username = data["data"]["username"]
            level = round(data["data"]["level"])
            userlvl = f"{username} - Level: {level}"
            #Headquarters Stats
            embed = discord.Embed(title=userlvl + " - Headquarters Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["mode"]["hq"]["properties"]["kills"] != "N/A":
                hqkills = round(data["data"]["lifetime"]["mode"]["hq"]["properties"]["kills"])
                hqdeaths = round(data["data"]["lifetime"]["mode"]["hq"]["properties"]["deaths"])
                hqcap = round(data["data"]["lifetime"]["mode"]["hq"]["properties"]["captures"])
                hqdef = round(data["data"]["lifetime"]["mode"]["hq"]["properties"]["defends"])
                hqkd = round(data["data"]["lifetime"]["mode"]["hq"]["properties"]["kdRatio"], 2)
                hqscore = round(data["data"]["lifetime"]["mode"]["hq"]["properties"]["score"])
                hqspm = round(data["data"]["lifetime"]["mode"]["hq"]["properties"]["scorePerMinute"], 2)
                hqtime = round(data["data"]["lifetime"]["mode"]["hq"]["properties"]["timePlayed"])
                embed.add_field(name="**Headquarters Stats**", value=f"**Kills:** {hqkills} \n **Deaths:** {hqdeaths} \n **Kill/Death Ratio:** {hqkd} \n **Captures:** {hqcap} \n **Defends:** {hqdef} \n **Score:** {hqscore} \n **Score Per Minute:** {hqspm} \n **Time Played:** {hqtime}", inline=True)
            if data["data"]["lifetime"]["mode"]["hc_hq"]["properties"]["kills"] != "N/A":
                hqkills = round(data["data"]["lifetime"]["mode"]["hc_hq"]["properties"]["kills"])
                hqdeaths = round(data["data"]["lifetime"]["mode"]["hc_hq"]["properties"]["deaths"])
                hqcap = round(data["data"]["lifetime"]["mode"]["hc_hq"]["properties"]["captures"])
                hqdef = round(data["data"]["lifetime"]["mode"]["hc_hq"]["properties"]["defends"])
                tdmkd = round(data["data"]["lifetime"]["mode"]["hc_hq"]["properties"]["kdRatio"], 2)
                tdmscore = round(data["data"]["lifetime"]["mode"]["hc_hq"]["properties"]["score"])
                tdmspm = round(data["data"]["lifetime"]["mode"]["hc_hq"]["properties"]["scorePerMinute"], 2)
                tdmtime = round(data["data"]["lifetime"]["mode"]["hc_hq"]["properties"]["timePlayed"])
                embed.add_field(name="**Hardcore Headquarters Stats**", value=f"**Kills:** {hqkills} \n **Deaths:** {hqdeaths} \n **Kill/Death Ratio:** {hqkd} \n **Captures:** {hqcap} \n **Defends:** {hqdef} \n **Score:** {hqscore} \n **Score Per Minute:** {hqspm} \n **Time Played:** {hqtime}", inline=True)
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=180
            )
        except:
            await ctx.send("Either the platform or username is incorrect, please make sure to use pc, psn or xbox for the platform and make sure you spelt your name correctly.")

    @commands.command()
    async def codkc(self, ctx, platform: Optional[str] = "", *, username: Optional[str] = ""):
        """Command to get your COD: MW kill confirmed stats
        For platform use pc, xbox, psn"""
        embeds = []
        if platform + username == "":
            user = ctx.author
            platform = await self.conf.user(user).platform()
            username = await self.conf.user(user).username()
        username = username.replace(" ", "%20")
        username = username.replace("#", "%23")
        platform = platform.replace("pc", "battle")
        platform = platform.replace("xbox", "xbl")
        async with self._session.get(
                f"https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/{platform}/gamer/{username}/profile/type/mp"
            ) as request:
                data = await request.json()
        
        try:
            username = data["data"]["username"]
            level = round(data["data"]["level"])
            userlvl = f"{username} - Level: {level}"
            #Kill Confirmed Stats
            embed = discord.Embed(title=userlvl + " - Kill Confirmed Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["mode"]["conf"]["properties"]["kills"] != "N/A":
                kckills = round(data["data"]["lifetime"]["mode"]["conf"]["properties"]["kills"])
                kcdeaths = round(data["data"]["lifetime"]["mode"]["conf"]["properties"]["deaths"])
                kccon = round(data["data"]["lifetime"]["mode"]["conf"]["properties"]["confirms"])
                kcden = round(data["data"]["lifetime"]["mode"]["conf"]["properties"]["denies"])
                kckd = round(data["data"]["lifetime"]["mode"]["conf"]["properties"]["kdRatio"], 2)
                kcscore = round(data["data"]["lifetime"]["mode"]["conf"]["properties"]["score"])
                kcspm = round(data["data"]["lifetime"]["mode"]["conf"]["properties"]["scorePerMinute"], 2)
                kctime = round(data["data"]["lifetime"]["mode"]["conf"]["properties"]["timePlayed"])
                embed.add_field(name="**Kill Confirmed Stats**", value=f"**Kills:** {kckills} \n **Deaths:** {kcdeaths} \n **Kill/Death Ratio:** {kckd} \n **Confirms:** {kccon} \n **Denies:** {kcden} \n **Score:** {kcscore} \n **Score Per Minute:** {kcspm} \n **Time Played:** {kctime}", inline=True)
            if data["data"]["lifetime"]["mode"]["hc_conf"]["properties"]["kills"] != "N/A":
                kckills = round(data["data"]["lifetime"]["mode"]["hc_conf"]["properties"]["kills"])
                kcdeaths = round(data["data"]["lifetime"]["mode"]["hc_conf"]["properties"]["deaths"])
                kccon = round(data["data"]["lifetime"]["mode"]["hc_conf"]["properties"]["confirms"])
                kcden = round(data["data"]["lifetime"]["mode"]["hc_conf"]["properties"]["denies"])
                kckd = round(data["data"]["lifetime"]["mode"]["hc_conf"]["properties"]["kdRatio"], 2)
                kcscore = round(data["data"]["lifetime"]["mode"]["hc_conf"]["properties"]["score"])
                kcspm = round(data["data"]["lifetime"]["mode"]["hc_conf"]["properties"]["scorePerMinute"], 2)
                kctime = round(data["data"]["lifetime"]["mode"]["hc_conf"]["properties"]["timePlayed"])
                embed.add_field(name="**Hardcore Kill Confirmed Stats**", value=f"**Kills:** {kckills} \n **Deaths:** {kcdeaths} \n **Kill/Death Ratio:** {kckd} \n **Confirms:** {kccon} \n **Denies:** {kcden} \n **Score:** {kcscore} \n **Score Per Minute:** {kcspm} \n **Time Played:** {kctime}", inline=True)
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=180
            )
        except:
            await ctx.send("Either the platform or username is incorrect, please make sure to use pc, psn or xbox for the platform and make sure you spelt your name correctly.")

    @commands.command()
    async def codsd(self, ctx, platform: Optional[str] = "", *, username: Optional[str] = ""):
        """Command to get your COD: MW search and destroy stats
        For platform use pc, xbox, psn"""
        embeds = []
        if platform + username == "":
            user = ctx.author
            platform = await self.conf.user(user).platform()
            username = await self.conf.user(user).username()
        username = username.replace(" ", "%20")
        username = username.replace("#", "%23")
        platform = platform.replace("pc", "battle")
        platform = platform.replace("xbox", "xbl")
        async with self._session.get(
                f"https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/{platform}/gamer/{username}/profile/type/mp"
            ) as request:
                data = await request.json()
        
        try:
            username = data["data"]["username"]
            level = round(data["data"]["level"])
            userlvl = f"{username} - Level: {level}"
            #Search and Destroy Stats
            embed = discord.Embed(title=userlvl + " - Search and Destroy Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["mode"]["sd"]["properties"]["kills"] != "N/A":
                sdkills = round(data["data"]["lifetime"]["mode"]["sd"]["properties"]["kills"])
                sddeaths = round(data["data"]["lifetime"]["mode"]["sd"]["properties"]["deaths"])
                sdplant = round(data["data"]["lifetime"]["mode"]["sd"]["properties"]["plants"])
                sddef = round(data["data"]["lifetime"]["mode"]["sd"]["properties"]["defuses"])
                sdkd = round(data["data"]["lifetime"]["mode"]["sd"]["properties"]["kdRatio"], 2)
                sdscore = round(data["data"]["lifetime"]["mode"]["sd"]["properties"]["score"])
                sdspm = round(data["data"]["lifetime"]["mode"]["sd"]["properties"]["scorePerMinute"], 2)
                sdtime = round(data["data"]["lifetime"]["mode"]["sd"]["properties"]["timePlayed"])
                embed.add_field(name="**Search and Destroy Stats**", value=f"**Kills:** {sdkills} \n **Deaths:** {sddeaths} \n **Kill/Death Ratio:** {sdkd} \n **Plants:** {sdplant} \n **Defuses:** {sddef} \n **Score:** {sdscore} \n **Score Per Minute:** {sdspm} \n **Time Played:** {sdtime}", inline=True)
            if data["data"]["lifetime"]["mode"]["hc_sd"]["properties"]["kills"] != "N/A":
                sdkills = round(data["data"]["lifetime"]["mode"]["hc_sd"]["properties"]["kills"])
                sddeaths = round(data["data"]["lifetime"]["mode"]["hc_sd"]["properties"]["deaths"])
                sdplant = round(data["data"]["lifetime"]["mode"]["hc_sd"]["properties"]["plants"])
                sddef = round(data["data"]["lifetime"]["mode"]["hc_sd"]["properties"]["defuses"])
                sdkd = round(data["data"]["lifetime"]["mode"]["hc_sd"]["properties"]["kdRatio"], 2)
                sdscore = round(data["data"]["lifetime"]["mode"]["hc_sd"]["properties"]["score"])
                sdspm = round(data["data"]["lifetime"]["mode"]["hc_sd"]["properties"]["scorePerMinute"], 2)
                sdtime = round(data["data"]["lifetime"]["mode"]["hc_sd"]["properties"]["timePlayed"])
                embed.add_field(name="**Hardcore Search and Destroy Stats**", value=f"**Kills:** {sdkills} \n **Deaths:** {sddeaths} \n **Kill/Death Ratio:** {sdkd} \n **Plants:** {sdplant} \n **Defuses:** {sddef} \n **Score:** {sdscore} \n **Score Per Minute:** {sdspm} \n **Time Played:** {sdtime}", inline=True)
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=180
            )
        except:
            await ctx.send("Either the platform or username is incorrect, please make sure to use pc, psn or xbox for the platform and make sure you spelt your name correctly.")

    @commands.command()
    async def codca(self, ctx, platform: Optional[str] = "", *, username: Optional[str] = ""):
        """Command to get your COD: MW cyber attack stats
        For platform use pc, xbox, psn"""
        embeds = []
        if platform + username == "":
            user = ctx.author
            platform = await self.conf.user(user).platform()
            username = await self.conf.user(user).username()
        username = username.replace(" ", "%20")
        username = username.replace("#", "%23")
        platform = platform.replace("pc", "battle")
        platform = platform.replace("xbox", "xbl")
        async with self._session.get(
                f"https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/{platform}/gamer/{username}/profile/type/mp"
            ) as request:
                data = await request.json()
        
        try:
            username = data["data"]["username"]
            level = round(data["data"]["level"])
            userlvl = f"{username} - Level: {level}"
            #Cyber Attack Stats
            embed = discord.Embed(title=userlvl + " - Cyber Attack Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["mode"]["cyber"]["properties"]["kills"] != "N/A":
                cykills = round(data["data"]["lifetime"]["mode"]["cyber"]["properties"]["kills"])
                cydeaths = round(data["data"]["lifetime"]["mode"]["cyber"]["properties"]["deaths"])
                cyplant = round(data["data"]["lifetime"]["mode"]["cyber"]["properties"]["plants"])
                cyrev = round(data["data"]["lifetime"]["mode"]["cyber"]["properties"]["revives"])
                cykd = round(data["data"]["lifetime"]["mode"]["cyber"]["properties"]["kdRatio"], 2)
                cyscore = round(data["data"]["lifetime"]["mode"]["cyber"]["properties"]["score"])
                cyspm = round(data["data"]["lifetime"]["mode"]["cyber"]["properties"]["scorePerMinute"], 2)
                cytime = round(data["data"]["lifetime"]["mode"]["cyber"]["properties"]["timePlayed"])
                embed.add_field(name="**Cyber Attack Stats**", value=f"**Kills:** {cykills} \n **Deaths:** {cydeaths} \n **Kill/Death Ratio:** {cykd} \n **Plants:** {cyplant} \n **Revives:** {cyrev} \n **Score:** {cyscore} \n **Score Per Minute:** {cyspm} \n **Time Played:** {cytime}", inline=True)
            if data["data"]["lifetime"]["mode"]["hc_cyber"]["properties"]["kills"] != "N/A":
                cykills = round(data["data"]["lifetime"]["mode"]["hc_cyber"]["properties"]["kills"])
                cydeaths = round(data["data"]["lifetime"]["mode"]["hc_cyber"]["properties"]["deaths"])
                cyplant = round(data["data"]["lifetime"]["mode"]["hc_cyber"]["properties"]["plants"])
                cyrev = round(data["data"]["lifetime"]["mode"]["hc_cyber"]["properties"]["revives"])
                cykd = round(data["data"]["lifetime"]["mode"]["hc_cyber"]["properties"]["kdRatio"], 2)
                cyscore = round(data["data"]["lifetime"]["mode"]["hc_cyber"]["properties"]["score"])
                cyspm = round(data["data"]["lifetime"]["mode"]["hc_cyber"]["properties"]["scorePerMinute"], 2)
                cytime = round(data["data"]["lifetime"]["mode"]["hc_cyber"]["properties"]["timePlayed"])
                embed.add_field(name="**Hardcore Cyber Attack Stats**", value=f"**Kills:** {cykills} \n **Deaths:** {cydeaths} \n **Kill/Death Ratio:** {cykd} \n **Plants:** {cyplant} \n **Defuses:** {cyrev} \n **Score:** {cyscore} \n **Score Per Minute:** {cyspm} \n **Time Played:** {cytime}", inline=True)
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=180
            )
        except:
            await ctx.send("Either the platform or username is incorrect, please make sure to use pc, psn or xbox for the platform and make sure you spelt your name correctly.")

    @commands.command()
    async def codhp(self, ctx, platform: Optional[str] = "", *, username: Optional[str] = ""):
        """Command to get your COD: MW hardpoint stats
        For platform use pc, xbox, psn"""
        embeds = []
        if platform + username == "":
            user = ctx.author
            platform = await self.conf.user(user).platform()
            username = await self.conf.user(user).username()
        username = username.replace(" ", "%20")
        username = username.replace("#", "%23")
        platform = platform.replace("pc", "battle")
        platform = platform.replace("xbox", "xbl")
        async with self._session.get(
                f"https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/{platform}/gamer/{username}/profile/type/mp"
            ) as request:
                data = await request.json()
        
        try:
            username = data["data"]["username"]
            level = round(data["data"]["level"])
            userlvl = f"{username} - Level: {level}"
            #HardPoint Stats
            embed = discord.Embed(title=userlvl + " - HardPoint Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["mode"]["koth"]["properties"]["kills"] != "N/A":
                hpkills = round(data["data"]["lifetime"]["mode"]["koth"]["properties"]["kills"])
                hpdeaths = round(data["data"]["lifetime"]["mode"]["koth"]["properties"]["deaths"])
                hpobjtime = round(data["data"]["lifetime"]["mode"]["koth"]["properties"]["objTime"])
                hpdef = round(data["data"]["lifetime"]["mode"]["koth"]["properties"]["defends"])
                hpkd = round(data["data"]["lifetime"]["mode"]["koth"]["properties"]["kdRatio"], 2)
                hpscore = round(data["data"]["lifetime"]["mode"]["koth"]["properties"]["score"])
                hpspm = round(data["data"]["lifetime"]["mode"]["koth"]["properties"]["scorePerMinute"], 2)
                hptime = round(data["data"]["lifetime"]["mode"]["koth"]["properties"]["timePlayed"])
                embed.add_field(name="**HardPoint Stats**", value=f"**Kills:** {hpkills} \n **Deaths:** {hpdeaths} \n **Kill/Death Ratio:** {hpkd} \n **Objective Time:** {hpobjtime} \n **Defends:** {hpdef} \n **Score:** {hpscore} \n **Score Per Minute:** {hpspm} \n **Time Played:** {hptime}", inline=True)
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=180
            )
        except:
            await ctx.send("Either the platform or username is incorrect, please make sure to use pc, psn or xbox for the platform and make sure you spelt your name correctly.")

    @commands.command()
    async def codweekly(self, ctx, platform: Optional[str] = "", *, username: Optional[str] = ""):
        """Command to get your COD: MW weekly stats
        For platform use pc, xbox, psn"""
        embeds = []
        if platform + username == "":
            user = ctx.author
            platform = await self.conf.user(user).platform()
            username = await self.conf.user(user).username()
        username = username.replace(" ", "%20")
        username = username.replace("#", "%23")
        platform = platform.replace("pc", "battle")
        platform = platform.replace("xbox", "xbl")
        async with self._session.get(
                f"https://my.callofduty.com/api/papi-client/stats/cod/v1/title/mw/platform/{platform}/gamer/{username}/profile/type/mp"
            ) as request:
                data = await request.json()
        
        try:
            username = data["data"]["username"]
            level = round(data["data"]["level"])
            userlvl = f"{username} - Level: {level}"
            #Weekly Stats
            embed = discord.Embed(title=userlvl + " - Weekly Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            try:
                if data["data"]["weekly"]["all"]["properties"]["medalXp"] != "N/A":
                    kills = round(data["data"]["weekly"]["all"]["properties"]["kills"])
                    embed.add_field(name="**Kills**", value=f"**{kills}**", inline=True)
                    deaths = round(data["data"]["weekly"]["all"]["properties"]["deaths"])
                    embed.add_field(name="**Deaths**", value=f"**{deaths}**", inline=True)
                    assists = round(data["data"]["weekly"]["all"]["properties"]["assists"])
                    embed.add_field(name="**Assists**", value=f"**{assists}**", inline=True)
                    kd = round(data["data"]["weekly"]["all"]["properties"]["kdRatio"])
                    embed.add_field(name="**Kill/Death Ratio**", value=f"**{kd}**", inline=True)
                    wins = round(data["data"]["weekly"]["all"]["properties"]["wins"])
                    embed.add_field(name="**Wins**", value=f"**{wins}**", inline=True)
                    losses = round(data["data"]["weekly"]["all"]["properties"]["losses"])
                    embed.add_field(name="**Losses**", value=f"**{losses}**", inline=True)
                    winlo = round(data["data"]["weekly"]["all"]["properties"]["wlRatio"])
                    embed.add_field(name="**Win/Loss Ratio**", value=f"**{winlo}**", inline=True)
                    score = round(data["data"]["weekly"]["all"]["properties"]["score"])
                    embed.add_field(name="**Score**", value=f"**{score}**", inline=True)
                    spm = round(data["data"]["weekly"]["all"]["properties"]["scorePerMinute"], 2)
                    embed.add_field(name="**Score Per Minute**", value=f"**{spm}**", inline=True)
                    matches = round(data["data"]["weekly"]["all"]["properties"]["matchesPlayed"])
                    embed.add_field(name="**Matches Played**", value=f"**{matches}**", inline=True)
                    long = round(data["data"]["weekly"]["all"]["properties"]["longestStreak"])
                    embed.add_field(name="**Highest Killstreak**", value=f"**{long}**", inline=True)
                    headshots = round(data["data"]["weekly"]["all"]["properties"]["headshots"])
                    embed.add_field(name="**headshots**", value=f"**{headshots}**", inline=True)
                    time = round(data["data"]["weekly"]["all"]["properties"]["timePlayed"])
                    embed.add_field(name="**Time Played**", value=f"**{time}**", inline=True)
            except:
                embed.add_field(name="**No Data**", value=f"There is no data for weekly stats for this user.", inline=True)
                embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=180
            )
        except:
            await ctx.send("Either the platform or username is incorrect, please make sure to use pc, psn or xbox for the platform and make sure you spelt your name correctly.")
