import discord
from discord.ext import commands

class Parzi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="parzi", aliases=["parzival"], description="parzi yazınca")
    async def parzi(self, ctx):
        if ctx.author.id == 1013951210035875882:  # Buraya sahibinizin Discord kullanıcı ID'sini girin
            await ctx.send("Sahibim")
        else:
            await ctx.send(" ? ")

def setup(bot):
    bot.add_cog(Parzi(bot))
