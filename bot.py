import discord
from discord.ext import commands
from discord import Embed
import json
import requests
import os
import asyncio

with open('./config.json', 'r+') as outfile:
    config = json.loads(outfile.read())

key = config["api"]["mainkey"]

allowedAuthorIDs = [
    723386696007155763,
    582385436983427075
]

bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or(config["bot"]["prefix"]), case_insensitive=True)



@bot.event
async def on_ready():
    print('Bot is online')


@bot.command(name="load", aliases=["lc"])
async def loadcog(ctx):
    running = True
    if ctx.author.id in allowedAuthorIDs:
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
    if ctx.author.id in allowedAuthorIDs:
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
    if ctx.author.id in allowedAuthorIDs:
        init_msg = await ctx.send(embed=Embed(title='ReLoad Cog', description='What type of cog are you reloading?\n:one: command\n:two: event'))
        for i in ['1️⃣', '2️⃣']:
            await init_msg.add_reaction(i)
        while running:
            reaction, user = await bot.wait_for('reaction_add', check=lambda reaction, user: reaction.message.channel == ctx.channel and user == ctx.author and reaction.message.id == init_msg.id)
            if reaction.emoji in ['1️⃣', '2️⃣']:
                break
            else:
                await ctx.send('No')
        if reaction.emoji == '1️⃣':
            await ctx.send(embed=Embed(description='What is the name of the cog you want reloaded.'))
            cog = await bot.wait_for('message', check=lambda cog: cog.channel.id == ctx.channel.id and cog.author == ctx.author)
            bot.unload_extension(f"commands.{cog.content}")
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

bot.remove_command('help')


if __name__ == "__main__":
    for filename in os.listdir("commands"):
        if filename.endswith(".py") and not filename.startswith("_"):
            bot.load_extension(f"commands.{filename[:-3]}")
    for filename in os.listdir('events'):
        if filename.endswith(".py") and not filename.startswith("_"):
            bot.load_extension(f'events.{filename[:-3]}')


bot.run(config["bot"]["token"])