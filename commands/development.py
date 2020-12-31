from discord.ext import commands
from discord import Embed
import json

with open('config.json', 'r+') as outfile:
    config = json.loads(outfile.read())

    
allowedAuthorIDs = config["allowedAuthorIDs"]

class Development(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.log_print("✅ Development cog loaded and ready")

    @commands.command(hidden=True, usage='shutdown')
    async def shutdown(self, ctx):
        """
        Makes the bot shutdown.
        """
        if ctx.author.id in allowedAuthorIDs:
            await self.log_print("⚙️ Shutdown run by {}".format(ctx.author))
            await ctx.send('Shutting Down...')
            try:
                await self.bot.close()
            except EnvironmentError:
                await self.log_print("⛔ EnvironmentError - Development")
                self.bot.clear()

    @commands.command(hidden=True, aliases=['cc'], usage='clearconsole')
    async def clearconsole(self, ctx):
        """
        This command clears the terminal.
        """
        if ctx.author.id in allowedAuthorIDs:
            for i in range(100):
                print('')
            print('Cleared\n\n')
            await ctx.send('Cleared')
            await self.log_print(f"⚙️ Console cleared.")

    @commands.command(name='reloadcmdcog', aliases=['rcc'], hidden=True, usage='reloadcmdcog <cog>')
    async def reload_command_cog(self, ctx, cog=None):
        """
        Reloads a command cog.
        """
        if ctx.author.id in allowedAuthorIDs:
            if not cog:
                await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description='Supply the command cog that you want reloaded.'))
            else:
                try:
                    await ctx.send(f'Reloading {cog} cog...')
                    self.bot.unload_extension(f"commands.{cog}")
                    self.bot.load_extension(f"commands.{cog}")
                    await ctx.send(f'{cog} cog has been reloaded')
                    await self.log_print(f"⚙️ `{cog}` command cog has been reloaded.")
                except commands.errors.ExtensionNotLoaded:
                    await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description='This cog was already loaded or could not be found'))
                except Exception as error:
                    await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description=str(error)), delete_after=600)
                    raise error





    @commands.command(name='reloadevtcog', aliases=['rec'], hidden=True, usage='reloadevtcog <cog>')
    async def reload_event_cog(self, ctx, cog=None):
        """
        Reloads an event cog.
        """
        if ctx.author.id in allowedAuthorIDs:
            if not cog:
                await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description='Supply the command cog that you want reloaded.'))
            else:
                try:
                    await ctx.send(f'Reloading {cog} cog...')
                    self.bot.unload_extension(f"events.{cog}")
                    self.bot.load_extension(f"events.{cog}")
                    await ctx.send(f'{cog} cog has been reloaded')
                    await self.log_print(f"⚙️ `{cog}` event cog has been reloaded.")
                except commands.errors.ExtensionNotLoaded:
                    await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description='This cog was already unloaded or could not be found'))
                except Exception as error:
                    await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description=str(error)), delete_after=600)
                    raise error

    @commands.command(name='unloadcmdcog', aliases=['ucc'], hidden=True, usage='unloadcmdcog <cog>')
    async def unload_command_cog(self, ctx, cog=None):
        """
        Unload a command cog.
        """
        if ctx.author.id in allowedAuthorIDs:
            if not cog:
                await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description='Supply the command cog that you want unloaded.'))
            else:
                try:
                    await ctx.send(f'Unloading {cog} cog...')
                    self.bot.unload_extension(f'commands.{cog}')
                    await ctx.send(f'{cog} cog has been unloaded')
                    await self.log_print(f"⚙️ `{cog}` command cog has been unloaded.")
                except commands.errors.ExtensionNotLoaded:
                    await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description='This cog was already unloaded or could not be found'))
                except Exception as error:
                    await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description=str(error)), delete_after=600)
                    raise error

    @commands.command(name='unloadevtcog', aliases=['uec'], hidden=True, usage='unloadevtcog <cog>')
    async def unload_event_cog(self, ctx, cog=None):
        """
        Unload a event cog.
        """
        if ctx.author.id in allowedAuthorIDs:
            if not cog:
                await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description='Supply the command cog that you want unloaded.'))
            else:
                try:
                    await ctx.send(f'Unloading {cog} cog...')
                    self.bot.unload_extension(f'events.{cog}')
                    await ctx.send(f'{cog} cog has been unloaded')
                    await self.log_print(f"⚙️ `{cog}` event cog has been unloaded.")
                except commands.errors.ExtensionNotLoaded:
                    await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description='This cog was already unloaded or could not be found'))
                except Exception as error:
                    await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description=str(error)), delete_after=600)
                    raise error


    @commands.command(name='loadcmdcog', aliases=['lcc'], hidden=True, usage='loadcmdcog <cog>')
    async def load_command_cog(self, ctx, cog=None):
        """
        Load a command cog.
        """
        if ctx.author.id in allowedAuthorIDs:
            if not cog:
                await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description='Supply the command cog that you want unloaded.'))
            else:
                try:
                    await ctx.send(f'Loading {cog} cog...')
                    self.bot.load_extension(f'commands.{cog}')
                    await ctx.send(f'{cog} cog has been loaded')
                    await self.log_print(f"⚙️ `{cog}` command cog has been loaded.")
                except commands.errors.ExtensionAlreadyLoaded:
                    await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description='This cog was already loaded or could not be found'))
                except commands.errors.ExtensionNotFound:
                    await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description=f'{cog} could not be found'))
                except Exception as error:
                    await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description=str(error)), delete_after=600)
                    raise error


    @commands.command(name='loadevtcog', aliases=['lec'], hidden=True, usage='loadevtcog <cog>')
    async def load_event_cog(self, ctx, cog=None):
        """
        Load a event cog.
        """
        if ctx.author.id in allowedAuthorIDs:
            if not cog:
                await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description='Supply the command cog that you want loaded.'))
            else:
                try:
                    await ctx.send(f'Loading {cog} cog...')
                    self.bot.load_extension(f'events.{cog}')
                    await ctx.send(f'{cog} cog has been loaded')
                    await self.log_print(f"⚙️ `{cog}` event cog has been loaded.")
                except commands.errors.ExtensionAlreadyLoaded:
                    await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description='This cog was already loaded.'))
                except commands.errors.ExtensionNotFound:
                    await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description=f'{cog} could not be found'))
                except Exception as error:
                    await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description=str(error)), delete_after=600)
                    raise error


    def log_print(self, message):
        print(message)
        channel = self.bot.get_channel(793364658563317790)
        return channel.send(message)

def setup(bot):
    bot.add_cog(Development(bot))