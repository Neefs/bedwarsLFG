from discord.ext import commands
from discord import Embed
import json
import datetime

class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.log_print('🕛 Error Cog has been loaded.')


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        else:
            cmd = ctx.command
            channel = self.bot.get_channel(793364658563317790)
            embed = Embed(title=':no_entry: Error :no_entry:', color=0xff0000)
            embed.add_field(name='Author', value=ctx.author.mention)
            embed.add_field(name='Channel', value=ctx.channel.mention)
            embed.add_field(name='Command', value=cmd.name, inline=False)
            embed.add_field(name='Error', value=error, inline=False)
            await channel.send(embed=embed)

                        
            data = {}
            data['errors'] = []
            data['errors'].append({
                'date': datetime.datetime.utcnow(),
                'command': f'{cmd.name}',
                'author': f'{ctx.author.id}',
                'channel': f'{ctx.channel}',
                'error': f'{error}'
            })

            with open('logs.json', 'w') as outfile:
                json.dump(data, outfile, indent=5)
            raise error



    def log_print(self, message):
        print(message)
        channel = self.bot.get_channel(793364658563317790)
        return channel.send(message)
    
def setup(bot):
    bot.add_cog(Errors(bot))
    