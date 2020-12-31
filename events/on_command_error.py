from discord.ext import commands
from discord import Embed

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
            raise error



    def log_print(self, message):
        print(message)
        channel = self.bot.get_channel(793364658563317790)
        return channel.send(message)
    
def setup(bot):
    bot.add_cog(Errors(bot))
    