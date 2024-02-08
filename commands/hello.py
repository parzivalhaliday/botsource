from discord.ext import commands

class Hello(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hello', help='Greet the user')
    async def hello(self, ctx):
        await ctx.send(f'Hello, {ctx.author.mention}!')

def setup(bot):
    bot.add_cog(Hello(bot))
