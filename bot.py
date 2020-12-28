import discord
from discord.ext import commands
from discord import Embed
import json
import requests
import os

with open('./config.json', 'r+') as outfile:
    config = json.loads(outfile.read())

key = config["api"]["mainkey"]

# TODO: Check If ingame discord matches discord account when registering.
# TODO: Give people a role and nick depending on star/prestige

bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or(config["bot"]["prefix"]))

def xp_to_star(XPLevel):
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

@bot.event
async def on_ready():
    print('Bot is online')

@bot.command()
async def sync(ctx, user):
    if ctx.author.id == 582385436983427075 or ctx.author.id == 779098822181388348 or ctx.author.id == 723386696007155763:  # pureqold or testing account or neefs
        hkey = config["api"]["mainkey"]
        data = requests.get("https://api.hypixel.net/player?key={}&name={}".format(hkey, user)).json()

        await ctx.send("Syncing Hypixel Stats for player '" + user + "'...")

        try:
            try:
                dcLink = data["player"]["socialMedia"]["links"]["DISCORD"]
                if str(dcLink) == str(ctx.author):
                    star = xp_to_star(data["player"]["stats"]["Bedwars"]["Experience"])
                    await ctx.author.edit(nick="[" + str(star) + "✫] " + user)

                    success = await ctx.send("Success!")
                    await success.add_reaction('✅')
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

@bot.command(name="load", aliases=["lc"])
async def loadcog(ctx):
    running = True
    if ctx.author.id == 723386696007155763:
        init_msg = await ctx.send(embed=Embed(title='Load Cog', description='What type of cog are you loading?\n:one: command\n:two: event'))
        for i in ['1️⃣', '2️⃣']:
            await init_msg.add_reaction(i)
        while running:
            reaction, user = await bot.wait_for('reaction_add', check=lambda reaction, user: reaction.message.channel == ctx.channel and user == ctx.author and reaction.message.id == init_msg.id)
            if reaction.emoji in ['1️⃣', '2️⃣']:
                print('broken')
                break
            else:
                await ctx.send('No')
        if reaction.emoji == '1️⃣':
            await ctx.send(embed=Embed(description='What is the name of the cog you want loaded.'))
            cog = await bot.wait_for('message', check=lambda cog: cog.channel.id == ctx.channel.id and cog.author.id == ctx.author.id)
            bot.load_extension(f"commands.{cog.content}")
            await ctx.send(embed=Embed(description=f"`{cog.content}` cog has been loaded."))
        elif reaction.emoji == '2️⃣':
            await ctx.send(embed=Embed(description='What is the name of the cog you want loaded.'))
            cog = await bot.wait_for('message', check=lambda cog: cog.channel.id == ctx.channel.id and cog.author.id == ctx.author.id)
            bot.load_extension(f"events.{cog.content}")
            await ctx.send(embed=Embed(description=f"`{cog.content}` cog has been loaded."))

    else:
        await ctx.send("No perm.", delete_after=5)

@bot.command(name="unload", aliases=["uc"])
async def unloadcog(ctx):
    running = True
    if ctx.author.id == 723386696007155763:
        init_msg = await ctx.send(embed=Embed(title='Unload Cog', description='What type of cog are you unloading?\n:one: command\n:two: event'))
        for i in ['1️⃣', '2️⃣']:
            await init_msg.add_reaction(i)
        while running:
            reaction, user = await bot.wait_for('reaction_add', check=lambda reaction, user: reaction.message.channel == ctx.channel and user == ctx.author and reaction.message.id == init_msg.id)
            if reaction.emoji in ['1️⃣', '2️⃣']:
                print('broken')
                break
            else:
                await ctx.send('No')
        if reaction.emoji == '1️⃣':
            await ctx.send(embed=Embed(description='What is the name of the cog you want unloaded.'))
            cog = await bot.wait_for('message', check=lambda cog: cog.channel.id == ctx.channel.id and cog.author == ctx.author)
            bot.unload_extension(f"commands.{cog.content}")
            await ctx.send(embed=Embed(description=f"`{cog.content}` cog has been unloaded."))
        elif reaction.emoji == '2️⃣':
            await ctx.send(embed=Embed(description='What is the name of the cog you want unloaded.'))
            cog = await bot.wait_for('message', check=lambda cog: cog.channel.id == ctx.channel.id and cog.author == ctx.author)
            bot.unload_extension(f"events.{cog}")
            await ctx.send(embed=Embed(description=f"`{cog}` cog has been unloaded."))

    else:
        await ctx.send("No perm.", delete_after=5)

@bot.command(aliases=["rc"])
async def reloadcog(ctx):
    running = True
    if ctx.author.id == 723386696007155763:
        init_msg = await ctx.send(embed=Embed(title='ReLoad Cog', description='What type of cog are you reloading?\n:one: command\n:two: event'))
        for i in ['1️⃣', '2️⃣']:
            await init_msg.add_reaction(i)
        while running:
            reaction, user = await bot.wait_for('reaction_add', check=lambda reaction, user: reaction.message.channel == ctx.channel and user == ctx.author and reaction.message.id == init_msg.id)
            if reaction.emoji in ['1️⃣', '2️⃣']:
                print('broken')
                break
            else:
                await ctx.send('No')
        if reaction.emoji == '1️⃣':
            await ctx.send(embed=Embed(description='What is the name of the cog you want reloaded.'))
            cog = await bot.wait_for('message', check=lambda cog: cog.channel.id == ctx.channel.id and cog.author == ctx.author)
            bot.unload_extension(f"commands.{cog.content}")
            await asyncio.sleep(2)
            bot.load_extension(f"commands.{cog.content}")
            await ctx.send(embed=Embed(description=f"`{cog.content}` cog has been reloaded."))
        elif reaction.emoji == '2️⃣':
            await ctx.send(embed=Embed(description='What is the name of the cog you want reloaded.'))
            cog = await bot.wait_for('message', check=lambda cog: cog.channel.id == ctx.channel.id and cog.author == ctx.author)
            await ctx.send(embed=Embed(description=f"`{cog.content}` cog is attemping to be reloaded."))
            bot.unload_extension(f'events.{cog.content}')
            await asyncio.sleep(2)
            bot.load_extension(f"events.{cog.content}")
            await ctx.send(embed=Embed(description=f"`{cog.content}` cog has been reloaded."))

    else:
        await ctx.send("No perm.", delete_after=5)

@loadcog.error
async def loadcog_error(ctx, error):
    if isinstance(error, commands.ExtensionAlreadyLoaded):
        await ctx.send("Already loaded")   
    elif isinstance(error, commands.ExtensionNotFound):
        await ctx.send("Not found") 
    else:
        raise error

@unloadcog.error
async def unloadcog_error(ctx, error):
    if isinstance(error, commands.ExtensionAlreadyLoaded):
        await ctx.send("Already loaded")   
    elif isinstance(error, commands.ExtensionNotFound):
        await ctx.send("Not found") 
    elif isinstance(error, commands.ExtensionNotLoaded):
        await ctx.send("Cog is already unloaded.")
    else:
        raise error

@reloadcog.error
async def reloadcog_error(ctx, error):
    if isinstance(error, commands.ExtensionAlreadyLoaded):
        await ctx.send("Already loaded")   
    elif isinstance(error, commands.ExtensionNotFound):
        await ctx.send("Not found") 
    elif isinstance(error, commands.ExtensionNotLoaded):
        await ctx.send("Cog not loaded. Load it using `-load <cogname>` and try again.")
    else:
        raise error





if __name__ == "__main__":
    for filename in os.listdir("commands"):
        if filename.endswith(".py") and not filename.startswith("_"):
            bot.load_extension(f"commands.{filename[:-3]}")
    for filename in os.listdir('events'):
        if filename.endswith(".py") and not filename.startswith("_"):
            bot.load_extension(f'events.{filename[:-3]}')


bot.run(config["bot"]["token"])