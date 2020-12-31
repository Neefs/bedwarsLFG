import discord
import jishaku
from discord.ext import commands
from discord import Embed
import json
import requests
import os
import asyncio

with open('./config.json', 'r+') as outfile:
    config = json.loads(outfile.read())

key = config["api"]["mainkey"]

allowedAuthorIDs = config["allowedAuthorIDs"]

bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or(config["bot"]["prefix"]), case_insensitive=True)



@bot.event
async def on_ready():
    try:
        bot.load_extension('jishaku')
    except commands.errors.ExtensionAlreadyLoaded:
        pass
    await log_print("✅ Bot online")



bot.remove_command('help')


if __name__ == "__main__":
    for filename in os.listdir("commands"):
        if filename.endswith(".py") and not filename.startswith("_"):
            bot.load_extension(f"commands.{filename[:-3]}")
    for filename in os.listdir('events'):
        if filename.endswith(".py") and not filename.startswith("_"):
            bot.load_extension(f'events.{filename[:-3]}')

def log_print(message):
    print(message)
    channel = bot.get_channel(793364658563317790)
    return channel.send(message)

bot.run(config["bot"]["token"])