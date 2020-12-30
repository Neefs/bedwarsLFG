import discord
from discord import Embed
from discord.ext import commands
from discord.utils import get
import requests
import json

prestiges = [
    "Stone",
    "Iron",
    "Gold",
    "Diamond",
    "Emerald",
    "Sapphire",
    "Ruby",
    "Crystal",
    "Opal",
    "Amethyst",
    "Rainbow",
    "Iron Prime",
    "Gold Prime",
    "Diamond Prime",
    "Emerald Prime",
    "Sapphire Prime",
    "Ruby Prime",
    "Crystal Prime",
    "Opal Prime",
    "Amethyst Prime",
    "Mirror",
    "Light",
    "Dawn",
    "Dusk",
    "Air",
    "Wind",
    "Nebula",
    "Earth",
    "Water",
    "Fire"
]

with open('./config.json', 'r+') as outfile:
    config = json.loads(outfile.read())

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Stats cog has been loaded.')

    @commands.command(name="stats", usage='stats <minecraft username>')
    async def stats(self, ctx, user):
        """
        Reveals the Bedwars stats of the specified user.
        """

        hkey = config["api"]["mainkey"]
        data = requests.get("https://api.hypixel.net/player?key={}&name={}".format(hkey, user)).json()

        await ctx.send("Attempting to load Bedwars stats of user '" + user + "'...")

        try:
            user = data["player"]["displayname"]
            gamesPlayed = data["player"]["stats"]["Bedwars"]["games_played_bedwars"]
            finalKills = data["player"]["stats"]["Bedwars"]["final_kills_bedwars"]
            bedsDestroyed = data["player"]["stats"]["Bedwars"]["beds_broken_bedwars"]
            bedsLost = data["player"]["stats"]["Bedwars"]["beds_lost_bedwars"]
            coins = data["player"]["stats"]["Bedwars"]["coins"]
            star = self.xp_to_star(data["player"]["stats"]["Bedwars"]["Experience"])
            prestige = self.find_prestige(star)
            if star in range(1, 1000):
                star = "[" + str(star) + "✫]"
            else:
                star = "[" + str(star) + "✪]"

            embed = Embed()
            embed.title = "📊 " + star + " " + user + "'s Bedwars Stats 📊"
            embed.color = 0x037ffc
            embed.add_field(name='Games Played', value=str(self.nice_str(gamesPlayed)))
            embed.add_field(name='Prestige', value=str(self.nice_str(prestige)))
            embed.add_field(name='Coins', value=str(self.nice_str(coins)))
            embed.add_field(name='Total Beds Broken', value=str(self.nice_str(bedsDestroyed)))
            embed.add_field(name='Total Beds Lost', value=str(self.nice_str(bedsLost)))
            embed.add_field(name='Beds Broken/Lost Ratio', value=str(self.nice_str(round(bedsDestroyed / bedsLost, 2))))
            embed.add_field(name='Total Final Kills', value=str(self.nice_str(finalKills)))
            await ctx.send(embed=embed)
        except TypeError:
            await ctx.send(embed=self.warning("This user does not exist or has never logged onto Hypixel."))

    def warning(self, message):
        embed = Embed()
        embed.color = 0xffff00
        embed.title = "⚠️ Warning ⚠️"
        embed.description = message
        return embed

    def xp_to_star(self, XPLevel):
        Star = 1
        XPLevelModified = XPLevel

        while True:
            if XPLevelModified > 487000:  # Reduce Prestige
                XPLevelModified -= 487000
                Star += 100  # add to stars
            else:  # now we have their prestige
                if XPLevelModified > 5000:  # Reduce the 5th star and beyond
                    XPLevelModified -= 5000
                    Star += 1  # add to stars
                else:  # now we have their 4-5th star
                    if XPLevelModified > 3500:  # Reduce the 4th star of the prestige
                        XPLevelModified -= 3500
                        Star += 1  # add to stars
                    else:  # now we have their 3-4th star
                        if XPLevelModified > 2000:  # Reduce the 3rd star of the prestige
                            XPLevelModified -= 2000
                            Star += 1  # add to stars
                        else:
                            if XPLevelModified > 1000:  # Reduce the 2nd star of the prestige
                                XPLevelModified -= 1000
                                Star += 1  # add to stars
                            else:
                                if XPLevelModified > 500:  # Reduce the 1st star of the prestige
                                    XPLevelModified -= 500
                                    Star += 1  # add to stars
                                else:
                                    break

        return Star

    def find_prestige(self, star):
        prestigeNum = 0
        while True:
            if star - 100 > 0:
                star -= 100
                prestigeNum += 1
            else:
                break
        return prestiges[prestigeNum]

    def nice_str(self, value):
        return "`" + str(value) + "`"

def setup(bot):
    bot.add_cog(Stats(bot))