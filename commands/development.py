from discord.ext import commands

class Development(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Development Cog loaded')

    @commands.command()
    async def shutdown(self, ctx):
        if ctx.author.id in [582385436983427075, 723386696007155763]:
            print("Shutdown run by {}".format(ctx.author))
            await ctx.send('Shutting Down...')
            try:
                await self.bot.close()
            except EnvironmentError:
                print('EnviornmentError')
                self.bot.clear()


def setup(bot):
    bot.add_cog(Development(bot))