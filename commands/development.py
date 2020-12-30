from discord.ext import commands
from discord import Embed

class Development(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Development Cog loaded')

    @commands.command(hidden=True, usage='shutdown')
    async def shutdown(self, ctx):
        """
        Makes the bot shutdown.
        """
        if ctx.author.id in [582385436983427075, 723386696007155763]:
            print("Shutdown run by {}".format(ctx.author))
            await ctx.send('Shutting Down...')
            try:
                await self.bot.close()
            except EnvironmentError:
                print('EnviornmentError')
                self.bot.clear()

    @commands.command(hidden=True, aliases=['cc'], usage='cc')
    async def clearconsole(self, ctx):
        """
        This command clears the terminal.
        """
        if ctx.author.id in [582385436983427075, 723386696007155763]:
            for i in range(100):
                print('')
            print('Cleared\n\n')
            await ctx.send('Cleared')

    @commands.command(name='reloadcmdcog', aliases=['rcc'], hidden=True, usage='rcc <cog>')
    async def reload_command_cog(self, ctx, cog=None):
        """
        Reloads a command cog.
        """
        if not cog:
            await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description='Supply the command cog that you want reloaded.'))
        else:
            try:
                await ctx.send(f'Reloading {cog} cog...')
                self.bot.unload_extension(f"commands.{cog}")
                self.bot.load_extension(f"commands.{cog}")
                await ctx.send(f'{cog} cog has been reloaded')
            except commands.errors.ExtensionNotLoaded:
                await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description='This cog was already loaded or could not be found'))
            except Exception as error:
                await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description=error), delete_after=600)
                raise error


    @commands.command(name='reloadevtcog', aliases=['rec'], hidden=True, usage='rec <cog>')
    async def reload_event_cog(self, ctx, cog=None):
        """
        Reloads an event cog.
        """
        if not cog:
            await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description='Supply the command cog that you want reloaded.'))
        else:
            try:
                await ctx.send(f'Reloading {cog} cog...')
                self.bot.unload_extension(f"events.{cog}")
                self.bot.load_extension(f"events.{cog}")
                await ctx.send(f'{cog} cog has been reloaded')
            except commands.errors.ExtensionNotLoaded:
                await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description='This cog was already loaded or could not be found'))
            except Exception as error:
                await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description=error), delete_after=600)
                raise error



def setup(bot):
    bot.add_cog(Development(bot))