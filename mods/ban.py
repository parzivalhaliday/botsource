import discord
from discord.ext import commands

class Mods(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="banla", description="Kullanıcıyı sunucudan yasaklar.")
    async def ban_user(self, ctx, member: commands.MemberConverter, *, reason="Neden belirtilmedi."):
        if ctx.author.id == 1013951210035875882:  # Sahip ID'sini değiştirin
            if member:
                await member.ban(reason=reason)
                await ctx.send(f"{member.mention} sunucudan yasaklandı. Sebep: {reason}")
            else:
                await ctx.send("Belirtilen kullanıcı bulunamadı.")
        else:
            await ctx.send("Parzii banlayamam :(")

def setup(bot):
    bot.add_cog(Mods(bot))
