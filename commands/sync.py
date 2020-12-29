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
    "Rainbow (1000+)",
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

allowedAuthorIDs = [
    723386696007155763,
    582385436983427075,
    779098822181388348
]

with open('./config.json', 'r+') as outfile:
    config = json.loads(outfile.read())


class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Sync Cog is ready.')

    @commands.command()
    async def sync(self, ctx, user):
        if ctx.author.id in allowedAuthorIDs:
            hkey = config["api"]["mainkey"]
            data = requests.get("https://api.hypixel.net/player?key={}&name={}".format(hkey, user)).json()

            await ctx.send("Syncing Hypixel Stats for player '" + user + "'...")

            try:
                try:
                    dcLink = data["player"]["socialMedia"]["links"]["DISCORD"]
                    if str(dcLink) == str(ctx.author):
                        star = self.xp_to_star(data["player"]["stats"]["Bedwars"]["Experience"])
                        await ctx.author.edit(nick="[" + str(star) + "✫] " + data["player"]["displayname"])

                        success = await ctx.send("Success!")
                        await success.add_reaction('✅')

                        prestige = self.find_prestige(star)

                        # Remove old prestige roles before updating
                        for role in ctx.author.roles:
                            if str(role) in prestiges:
                                await ctx.author.remove_roles(role)
                                print("Removed role " + str(role) + " from player " + str(ctx.author))

                        role = get(ctx.author.guild.roles, name=prestige)
                        await ctx.author.add_roles(role)
                    else:
                        warning = await ctx.send(user + "'s Discord Username does not match " + str(ctx.author).split("#")[0] + "'s Discord Username!")
                        await warning.add_reaction('🚫')
                except KeyError:
                    warning = await ctx.send("This user does not have their Discord linked on their Hypixel Social Media menu.")
                    await warning.add_reaction('⚠️')
            except TypeError:
                warning = await ctx.send("This user does not exist or has never logged onto Hypixel.")
                await warning.add_reaction('⚠️')
        else:
            await ctx.send("No perm.", delete_after=5)

    @commands.command()
    async def devsync(self, ctx, dc: discord.Member, user):
        if ctx.author.id in allowedAuthorIDs:
            hkey = config["api"]["mainkey"]
            data = requests.get("https://api.hypixel.net/player?key={}&name={}".format(hkey, user)).json()

            await ctx.send("Syncing Hypixel Stats for player '" + user + "'...")

            try:
                try:
                    dcLink = data["player"]["socialMedia"]["links"]["DISCORD"]
                    if str(dcLink) == str(dc):
                        star = self.xp_to_star(data["player"]["stats"]["Bedwars"]["Experience"])
                        await dc.edit(nick="[" + str(star) + "✫] " + data["player"]["displayname"])

                        success = await ctx.send("Success!")
                        await success.add_reaction('✅')

                        prestige = self.find_prestige(star)
                        role = get(dc.guild.roles, name=prestige)
                        await dc.add_roles(role)
                    else:
                        warning = await ctx.send(user + "'s Discord Username does not match " + str(dc).split("#")[0] + "'s Discord Username!")
                        await warning.add_reaction('🚫')
                except KeyError:
                    warning = await ctx.send("This user does not have their Discord linked on their Hypixel Social Media menu.")
                    await warning.add_reaction('⚠️')
            except TypeError:
                warning = await ctx.send("This user does not exist or has never logged onto Hypixel.")
                await warning.add_reaction('⚠️')
        else:
            await ctx.send("No perm.", delete_after=5)

    @commands.command()
    async def forcesync(self, ctx, dc: discord.Member, user):
        # This will be used for someone that can't link there discord for whatever reason. Such as special chars
        if any([i for i in ctx.author.roles if i.id in [720281829810241559, 792634123965169706, 792643071699189770, 792642253843464202]]):
            hkey = config["api"]["mainkey"]
            data = requests.get("https://api.hypixel.net/player?key={}&name={}".format(hkey, user)).json()

            try:
                await ctx.send("Syncing Hypixel Stats for player '" + user + "'...")

                try:
                    star = self.xp_to_star(data["player"]["stats"]["Bedwars"]["Experience"])
                    await dc.edit(nick="[" + str(star) + "✫] " + data["player"]["displayname"])

                    success = await ctx.send("Success!")
                    await success.add_reaction('✅')

                    prestige = self.find_prestige(star)

                    # Remove old prestige roles before updating
                    for role in ctx.author.roles:
                        if str(role) in prestiges:
                            await ctx.author.remove_roles(role)
                            print("Removed role " + str(role) + " from player " + str(ctx.author))

                    role = get(dc.guild.roles, name=prestige)
                    await dc.add_roles(role)
                except KeyError:
                    warning = await ctx.send("This user does not have their Discord linked on their Hypixel Social Media menu.")
                    await warning.add_reaction('⚠️')
            except TypeError:
                warning = await ctx.send("The user '" + user + "' does not exist!")
                await warning.add_reaction('🚫')
        else:
            await ctx.send('No perms.')

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

def setup(bot):
    bot.add_cog(Sync(bot))