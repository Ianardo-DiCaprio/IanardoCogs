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
                embed.add_field(name="**Total Headshots**", value=headshots, inline=True)
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
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_kilo433"]["properties"]["headShots"])
                embed.add_field(name="**Kilo 141 Stats**", value=f"**Kills:** {kilo} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_mike4"]["properties"]["kills"] != "N/A":
                m4a1 = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_mike4"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_mike4"]["properties"]["headShots"])
                embed.add_field(name="**M4A1 Stats**", value=f"**Kills:** {m4a1} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_falpha"]["properties"]["kills"] != "N/A":
                FR = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_falpha"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_falpha"]["properties"]["headShots"])
                embed.add_field(name="**FR 5.56 Stats**", value=f"**Kills:** {FR} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_asierra12"]["properties"]["kills"] != "N/A":
                oden = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_asierra12"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_asierra12"]["properties"]["headShots"])
                embed.add_field(name="**Oden Stats**", value=f"**Kills:** {oden} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_akilo47"]["properties"]["kills"] != "N/A":
                ak = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_akilo47"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_akilo47"]["properties"]["headShots"])
                embed.add_field(name="**AK-47 Stats**", value=f"**Kills:** {ak} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_scharlie"]["properties"]["kills"] != "N/A":
                scar = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_scharlie"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_scharlie"]["properties"]["headShots"])
                embed.add_field(name="**FN Scar 17 Stats**", value=f"**Kills:** {scar} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_falima"]["properties"]["kills"] != "N/A":
                fal = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_falima"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_falima"]["properties"]["headShots"])
                embed.add_field(name="**FAL Stats**", value=f"**Kills:** {fal} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_mcharlie"]["properties"]["kills"] != "N/A":
                m13 = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_mcharlie"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_assault_rifle"]["iw8_ar_mcharlie"]["properties"]["headShots"])
                embed.add_field(name="**M13 Stats**", value=f"**Kills:** {m13} \n **Headshots:** {headshots}", inline=True)
            embeds.append(embed)
            #LMG Stats
            embed = discord.Embed(title=userlvl + " - LMG Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_kilo121"]["properties"]["kills"] != "N/A":
                m91 = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_kilo121"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_kilo121"]["properties"]["headShots"])
                embed.add_field(name="**M91 Stats**", value=f"**Kills:** {m91} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_lima86"]["properties"]["kills"] != "N/A":
                sa87 = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_lima86"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_lima86"]["properties"]["headShots"])
                embed.add_field(name="**SA87 Stats**", value=f"**Kills:** {sa87} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_mgolf34"]["properties"]["kills"] != "N/A":
                mg34 = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_mgolf34"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_mgolf34"]["properties"]["headShots"])
                embed.add_field(name="**MG34 Stats**", value=f"**Kills:** {mg34} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_pkilo"]["properties"]["kills"] != "N/A":
                pkm = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_pkilo"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_pkilo"]["properties"]["headShots"])
                embed.add_field(name="**PKM Stats**", value=f"**Kills:** {pkm} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_dblmg"]["properties"]["kills"] != "N/A":
                holger = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_dblmg"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_lmg"]["iw8_lm_dblmg"]["properties"]["headShots"])
                embed.add_field(name="**Holger-26 Stats**", value=f"**Kills:** {holger} \n **Headshots:** {headshots}", inline=True)
            embeds.append(embed)
            #Launcher Stats
            embed = discord.Embed(title=userlvl + " - Launcher Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_gromeo"]["properties"]["kills"] != "N/A":
                pila = round(data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_gromeo"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_gromeo"]["properties"]["headShots"])
                embed.add_field(name="**PILA Stats**", value=f"**Kills:** {pila} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_rpapa7"]["properties"]["kills"] != "N/A":
                rpg = round(data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_rpapa7"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_rpapa7"]["properties"]["headShots"])
                embed.add_field(name="**RPG-7 Stats**", value=f"**Kills:** {rpg} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_juliet"]["properties"]["kills"] != "N/A":
                jokr = round(data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_juliet"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_juliet"]["properties"]["headShots"])
                embed.add_field(name="**JOKR Stats**", value=f"**Kills:** {jokr} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_kgolf"]["properties"]["kills"] != "N/A":
                strella = round(data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_kgolf"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_launcher"]["iw8_la_kgolf"]["properties"]["headShots"])
                embed.add_field(name="**Strella-P Stats**", value=f"**Kills:** {strella} \n **Headshots:** {headshots}", inline=True)
            embeds.append(embed)
            #Pistol Stats
            embed = discord.Embed(title=userlvl + " - Pistol Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_decho"]["properties"]["kills"] != "N/A":
                gs = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_decho"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_decho"]["properties"]["headShots"])
                embed.add_field(name="**.50 GS Stats**", value=f"**Kills:** {gs} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_cpapa"]["properties"]["kills"] != "N/A":
                revol = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_cpapa"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_cpapa"]["properties"]["headShots"])
                embed.add_field(name="**.357 Stats**", value=f"**Kills:** {revol} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_mike1911"]["properties"]["kills"] != "N/A":
                m1911 = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_mike1911"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_mike1911"]["properties"]["headShots"])
                embed.add_field(name="**1911 Stats**", value=f"**Kills:** {m1911} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_golf21"]["properties"]["kills"] != "N/A":
                x16 = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_golf21"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_golf21"]["properties"]["headShots"])
                embed.add_field(name="**X16 Stats**", value=f"**Kills:** {x16} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_papa320"]["properties"]["kills"] != "N/A":
                m19 = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_papa320"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_pistol"]["iw8_pi_papa320"]["properties"]["headShots"])
                embed.add_field(name="**M19 Stats**", value=f"**Kills:** {m19} \n **Headshots:** {headshots}", inline=True)
            embeds.append(embed)
            #Shotgun Stats
            embed = discord.Embed(title=userlvl + " - Shotgun Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_charlie725"]["properties"]["kills"] != "N/A":
                farmer = round(data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_charlie725"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_charlie725"]["properties"]["headShots"])
                embed.add_field(name="**725 Stats**", value=f"**Kills:** {farmer} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_romeo870"]["properties"]["kills"] != "N/A":
                model = round(data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_romeo870"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_romeo870"]["properties"]["headShots"])
                embed.add_field(name="**Model 680 Stats**", value=f"**Kills:** {model} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_oscar12"]["properties"]["kills"] != "N/A":
                origin = round(data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_oscar12"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_oscar12"]["properties"]["headShots"])
                embed.add_field(name="**Origin 12 Shotgun Stats**", value=f"**Kills:** {origin} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_dpapa12"]["properties"]["kills"] != "N/A":
                r9 = round(data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_dpapa12"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_shotgun"]["iw8_sh_dpapa12"]["properties"]["headShots"])
                embed.add_field(name="**R9-0 Shotgun Stats**", value=f"**Kills:** {r9} \n **Headshots:** {headshots}", inline=True)
            embeds.append(embed)
            #SMG Stats
            embed = discord.Embed(title=userlvl + " - SMG Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_mpapa7"]["properties"]["kills"] != "N/A":
                mp7 = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_mpapa7"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_mpapa7"]["properties"]["headShots"])
                embed.add_field(name="**MP7 Stats**", value=f"**Kills:** {mp7} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_augolf"]["properties"]["kills"] != "N/A":
                aug = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_augolf"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_augolf"]["properties"]["headShots"])
                embed.add_field(name="**AUG Stats**", value=f"**Kills:** {aug} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_papa90"]["properties"]["kills"] != "N/A":
                p90 = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_papa90"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_papa90"]["properties"]["headShots"])
                embed.add_field(name="**P90 Stats**", value=f"**Kills:** {p90} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_mpapa5"]["properties"]["kills"] != "N/A":
                mp5 = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_mpapa5"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_mpapa5"]["properties"]["headShots"])
                embed.add_field(name="**MP5 Stats**", value=f"**Kills:** {mp5} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_beta"]["properties"]["kills"] != "N/A":
                bizon = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_beta"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_beta"]["properties"]["headShots"])
                embed.add_field(name="**PP19 Bizon Stats**", value=f"**Kills:** {bizon} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_uzulu"]["properties"]["kills"] != "N/A":
                uzi = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_uzulu"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_smg"]["iw8_sm_uzulu"]["properties"]["headShots"])
                embed.add_field(name="**Uzi Stats**", value=f"**Kills:** {uzi} \n **Headshots:** {headshots}", inline=True)
            embeds.append(embed)
            #Sniper Rifle Stats
            embed = discord.Embed(title=userlvl + " - Sniper Rifle Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["weapon_sniper"]["iw8_sn_hdromeo"]["properties"]["kills"] != "N/A":
                hdr = round(data["data"]["lifetime"]["itemData"]["weapon_sniper"]["iw8_sn_hdromeo"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_sniper"]["iw8_sn_hdromeo"]["properties"]["headShots"])
                embed.add_field(name="**HDR Stats**", value=f"**Kills:** {hdr} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_sniper"]["iw8_sn_alpha50"]["properties"]["kills"] != "N/A":
                ax = round(data["data"]["lifetime"]["itemData"]["weapon_sniper"]["iw8_sn_alpha50"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_sniper"]["iw8_sn_alpha50"]["properties"]["headShots"])
                embed.add_field(name="**AX-50 Stats**", value=f"**Kills:** {ax} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_dmr"]["iw8_sn_delta"]["properties"]["kills"] != "N/A":
                drag = round(data["data"]["lifetime"]["itemData"]["weapon_dmr"]["iw8_sn_delta"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_dmr"]["iw8_sn_delta"]["properties"]["headShots"])
                embed.add_field(name="**Dragunov Stats**", value=f"**Kills:** {drag} \n **Headshots:** {headshots}", inline=True)
            embeds.append(embed)
            #Marksman Rifle Stats
            embed = discord.Embed(title=userlvl + " - Marksman Rifle Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["itemData"]["weapon_dmr"]["iw8_sn_kilo98"]["properties"]["kills"] != "N/A":
                kar = round(data["data"]["lifetime"]["itemData"]["weapon_dmr"]["iw8_sn_kilo98"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_dmr"]["iw8_sn_kilo98"]["properties"]["headShots"])
                embed.add_field(name="**Kar98K Stats**", value=f"**Kills:** {kar} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_sniper"]["iw8_sn_sbeta"]["properties"]["kills"] != "N/A":
                carbine = round(data["data"]["lifetime"]["itemData"]["weapon_sniper"]["iw8_sn_sbeta"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_sniper"]["iw8_sn_sbeta"]["properties"]["headShots"])
                embed.add_field(name="**MK2 Carbine Stats**", value=f"**Kills:** {carbine} \n **Headshots:** {headshots}", inline=True)
            if data["data"]["lifetime"]["itemData"]["weapon_dmr"]["iw8_sn_mike14"]["properties"]["kills"] != "N/A":
                ebr = round(data["data"]["lifetime"]["itemData"]["weapon_dmr"]["iw8_sn_mike14"]["properties"]["kills"])
                headshots = round(data["data"]["lifetime"]["itemData"]["weapon_dmr"]["iw8_sn_mike14"]["properties"]["headShots"])
                embed.add_field(name="**EBR-14 Stats**", value=f"**Kills:** {ebr} \n **Headshots:** {headshots}", inline=True)
            embeds.append(embed)
            #DOM Stats
            embed = discord.Embed(title=userlvl + " - Marksman Rifle Stats", color=0x8C05D2)
            embed.set_thumbnail(url="https://i.pinimg.com/originals/cb/ea/43/cbea438a032192c7aa8210e596e4c065.png")
            embed.set_footer(text="React to change pages for more stats!")
            if data["data"]["lifetime"]["mode"]["dom"]["properties"]["kills"] != "N/A":
                domkills = round(data["data"]["lifetime"]["mode"]["dom"]["properties"]["kills"])
                embed.add_field(name="**Dom Stats**", value=f"**Kills:** {domkills}", inline=True)
            embeds.append(embed)
            await menu(
                ctx, pages=embeds, controls=DEFAULT_CONTROLS, message=None, page=0, timeout=180
            )
        except:
            await ctx.send("Either the platform or username is incorrect, please make sure to use pc, psn or xbox for the platform and make sure you spelt your name correctly.")
                                                                                                    