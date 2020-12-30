from discord.ext import commands
from discord import Embed

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x6a0dad
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Help cog has been loaded.')

    @commands.command(name="help", usage='help [command]')
    async def help_command(self, ctx: commands.Context, *, search: str = None):
        """
        This command shows you what basic information on other commands.
        """
        if not search:
            embed = Embed(color=self.color, title='Help')
            cogs = self.bot.cogs
            cmdsl = []
            for cog in cogs:
                cmdsl.clear()
                
                cog_commands = self.bot.get_cog(cog).get_commands()
                for cmd in cog_commands:
                    if await cmd.can_run(ctx) and ctx.author.guild_permissions.administrator or not cmd.hidden:
                        cmdsl.append(cmd.name)
                
                cmds = ""
                for i in cmdsl:
                    if i == cmdsl[len(cmdsl) - 1]: # it is the last item in this list
                        cmds += i # just add to string
                    else:
                        cmds += (i + ", ") # add to string with comma and space
                if cmds == "":
                    pass
                else:
                    embed.add_field(name=cog, value=cmds, inline=False)
            await ctx.send(embed=embed)
                
                
        else:
            cmd = self.bot.get_command(search)
            try:
                if await cmd.can_run(ctx) and ctx.author.guild_permissions.administrator or not cmd.hidden:
                    embed = Embed()
                    embed.title = "Command: {}".format(cmd.name)
                    embed.color = self.color
                    embed.add_field(name='Description', value=cmd.help)
                    if not cmd.usage:
                        embed.add_field(name='Usage', value=None)
                    else:
                        embed.add_field(name='Usage', value='-'+cmd.usage)
                    embed.set_footer(text='<> = Required [] = Optional')
                    await ctx.send(embed=embed)
            except AttributeError:
                await ctx.send(embed=Embed(color=0xff0000, title='⛔ Error ⛔', description='That is not a valid help option.\nDo -help to see the options.'))
                


def setup(bot):
    bot.add_cog(Help(bot))