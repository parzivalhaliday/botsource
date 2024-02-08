import discord
from discord.ext import commands

class SetNickname(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setnickname')
    async def set_nickname(self, ctx, member: discord.Member, *, new_nickname):
        try:
            await member.edit(nick=new_nickname)
            await ctx.send(f"{member.mention} kullanıcısının takma adı başarıyla güncellendi: {new_nickname}")
        except Exception as e:
            await ctx.send(f"Hata: {e}")

def setup(bot):
    bot.add_cog(SetNickname(bot))
