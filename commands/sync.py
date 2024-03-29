import discord
from discord import Embed
from discord.ext import commands
from discord.utils import get
import requests
import json

# TODO: Make all messages send in an embed
# TODO: Delete messages after a certain point. Like 60 seconds to reduce the bot spam.
# TODO: Add Error handling. so if someone types -sync it doesnt break
# TODO: Add some logging.

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


    
allowedAuthorIDs = config["allowedAuthorIDs"]





class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.log_print("✅ Sync cog loaded and ready")

    @commands.command(usage='sync <mincecraft username>')
    async def sync(self, ctx, user):
        """
        Syncs your bedwars stats with this discord. Gives you a nickname depending on your stars and a role depending on your prestige.
        **Requires your discord to be linked with your hypixel account.**
        """
        if ctx.author.id in allowedAuthorIDs:
            hkey = config["api"]["mainkey"]
            uuid = requests.get("https://api.mojang.com/users/profiles/minecraft/{}".format(user)).json()
            data = requests.get("https://api.hypixel.net/player?key={}&uuid={}".format(hkey, uuid["id"])).json()
            

            await ctx.send("Syncing Hypixel Stats for player '" + user + "'...")

            try:
                try:
                    dcLink = data["player"]["socialMedia"]["links"]["DISCORD"]
                except KeyError:
                    await ctx.send(embed=self.warning("This user does not have their Discord linked on their Hypixel Social Media menu."))
                    return
                else:
                    if str(dcLink) == str(ctx.author):
                        star = data["player"]["achievements"]["bedwars_level"]
                        if star in range(1, 1000):
                            await ctx.author.edit(nick="[" + str(star) + "✫] " + data["player"]["displayname"])
                        else:
                            await ctx.author.edit(nick="[" + str(star) + "✪] " + data["player"]["displayname"])

                        await ctx.send(embed=self.success("Bedwars stats successfully synced with Discord!", star))

                        prestige = self.find_prestige(star)

                        # Remove old prestige roles before updating
                        for role in ctx.author.roles:
                            if str(role) in prestiges:
                                await ctx.author.remove_roles(role)
                                print("Removed role " + str(role) + " from player " + str(ctx.author))

                        role = get(ctx.author.guild.roles, name=prestige)
                        await ctx.author.add_roles(role)
                    else:
                        await ctx.send(embed=self.warning(user + "'s Discord Username does not match " + str(ctx.author).split("#")[0] + "'s Discord Username!"))
                            
                
                    
            except TypeError:
                await ctx.send(embed=self.warning("This user does not exist or has never logged onto Hypixel."))
                
        else:
            await ctx.send("No perm.", delete_after=5)

    @sync.error
    async def sync_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            cmd = self.bot.get_command('sync')
            await ctx.send(embed=self.error(f'Type: **Invalid Syntax**\nUsage: -{cmd.usage}'))
        else:
            raise error

    @commands.command(hidden=True, usage='devsync <@user or id> <MC username>')
    async def devsync(self, ctx, dc: discord.Member, user):
        """
        This command is for testing purposes. It is run by developers to determine errors.
        """
        if ctx.author.id in allowedAuthorIDs:
            hkey = config["api"]["mainkey"]
            uuid = requests.get("https://api.mojang.com/users/profiles/minecraft/{}".format(user)).json()
            data = requests.get("https://api.hypixel.net/player?key={}&uuid={}".format(hkey, uuid["id"])).json()
            
            await ctx.send("Syncing Hypixel Stats for player '" + user + "'...")

            try:
                try:
                    dcLink = data["player"]["socialMedia"]["links"]["DISCORD"]
                    if str(dcLink) == str(dc):
                        star = data["player"]["achievements"]["bedwars_level"]
                        if star in range(1, 1000):
                            await dc.edit(nick="[" + str(star) + "✫] " + data["player"]["displayname"])
                        else:
                            await dc.edit(nick="[" + str(star) + "✪] " + data["player"]["displayname"])

                        await ctx.send(embed=self.success("Bedwars stats successfully synced with Discord!", star))

                        prestige = self.find_prestige(star)
                        role = get(dc.guild.roles, name=prestige)
                        await dc.add_roles(role)
                    else:
                        await ctx.send(embed=self.warning(user + "'s Discord Username does not match " + str(ctx.author).split("#")[0] + "'s Discord Username!"))
                except KeyError:
                    await ctx.send(embed=self.warning("This user does not have their Discord linked on their Hypixel Social Media menu."))
                    
            except TypeError:
                await ctx.send(embed=self.warning("This user does not exist or has never logged onto Hypixel."))
                
        else:
            await ctx.send("No perm.", delete_after=5)

    @commands.command(usage='forcesync <@user or id> <MC username>')
    async def forcesync(self, ctx, dc: discord.Member, user):
        """
        This command is used by moderators to forcibly sync someone without having there discord linked.
        This will most likely be used if there discord name has a special characters.
        """
        # This will be used for someone that can't link there discord for whatever reason. Such as special chars
        if any([i for i in ctx.author.roles if i.id in [720281829810241559, 792634123965169706, 792643071699189770, 792642253843464202]]):
            hkey = config["api"]["mainkey"]
            uuid = requests.get("https://api.mojang.com/users/profiles/minecraft/{}".format(user)).json()
            data = requests.get("https://api.hypixel.net/player?key={}&uuid={}".format(hkey, uuid["id"])).json()
            
            try:
                await ctx.send("Syncing Hypixel Stats for player '" + user + "'...")

                
                star = data["player"]["achievements"]["bedwars_level"]
                if star in range(1, 1000):
                    await dc.edit(nick="[" + str(star) + "✫] " + data["player"]["displayname"])
                else:
                    await dc.edit(nick="[" + str(star) + "✪] " + data["player"]["displayname"])

                await ctx.send(embed=self.success("Bedwars stats successfully synced with Discord!", star))

                prestige = self.find_prestige(star)

                # Remove old prestige roles before updating
                for role in ctx.author.roles:
                    if str(role) in prestiges:
                        await ctx.author.remove_roles(role)
                        print("Removed role " + str(role) + " from player " + str(ctx.author))

                role = get(dc.guild.roles, name=prestige)
                await dc.add_roles(role)
                   
            except TypeError:
                await ctx.send(embed=self.warning("The user '" + user + "' does not exist!"))
        else:
            await ctx.send('No perms.')


    def find_prestige(self, star):
        prestigeNum = 0
        while True:
            if star - 100 > 0:
                star -= 100
                prestigeNum += 1
            else:
                break
        return prestiges[prestigeNum]

    def warning(self, message):
        embed = Embed()
        embed.color = 0xffff00
        embed.title = "⚠️ Warning ⚠️"
        embed.description = message
        return embed

    def error(self, message):
        embed = Embed()
        embed.color = 0xff0000
        embed.title = "⛔ Error ⛔"
        embed.description = message
        return embed

    def success(self, message, star):
        embed = Embed()
        embed.color = 0x8cfc03
        embed.title = "✅ Success ✅"
        embed.description = message
        embed.set_footer(text="Your Bedwars star: " + str(star))
        return embed

    def log_print(self, message):
        print(message)
        channel = self.bot.get_channel(793364658563317790)
        return channel.send(message)

def setup(bot):
    bot.add_cog(Sync(bot))