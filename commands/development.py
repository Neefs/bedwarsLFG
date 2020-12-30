from discord.ext import commands
from discord import Embed

class Development(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Development Cog loaded')

    @commands.command(hidden=True)
    async def shutdown(self, ctx):
        if ctx.author.id in [582385436983427075, 723386696007155763]:
            print("Shutdown run by {}".format(ctx.author))
            await ctx.send('Shutting Down...')
            try:
                await self.bot.close()
            except EnvironmentError:
                print('EnviornmentError')
                self.bot.clear()

    @commands.command(hidden=True, aliases=['cc'])
    async def clearconsole(self, ctx):
        if ctx.author.id in [582385436983427075, 723386696007155763]:
            for i in range(100):
                print('')
            print('Cleared\n\n')
            await ctx.send('Cleared')

    @commands.command(name='reloadcmdcog', aliases=['rcc'])
    async def reload_command_cog(self, ctx, cog=None):
        if not cog:
            await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description='Supply the command cog that you want reloaded.'))
        else:
            try:
                await ctx.send(f'Reloading {cog} cog...')
                self.bot.unload_extension(f"commands.{cog}")
                self.bot.load_extension(f"commands.{cog}")
                await ctx.send(f'{cog} cog has been reloaded')
            except Ex
            except Exception as error:
                await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description=error), delete_after=600)
                raise error



def setup(bot):
    bot.add_cog(Development(bot))