import discord
from discord.ext import commands

class Sil(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sil", description="Mesajları silme")
    @commands.has_permissions(manage_messages=True)
    async def sil(self, ctx, amount: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)

def setup(bot):
    cog_name = "Sil"
    if cog_name not in bot.cogs:
        bot.add_cog(Sil(bot))
    else:
        print(f"Cog named '{cog_name}' already loaded")
