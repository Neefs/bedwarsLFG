from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Help cog has been loaded.')


def setup(bot):
    bot.add_cog(Help(bot))