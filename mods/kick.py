import discord
from discord.ext import commands

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kick', help='Belirtilen kullanıcıyı sunucudan atar. Kullanım: !kick <user_id>')
    async def kick(self, ctx, user_id: int):
        # Sadece yetkililerin kullanabileceği bir komut
        if ctx.author.guild_permissions.kick_members:
            try:
                user = await self.bot.fetch_user(user_id)
                member = await ctx.guild.fetch_member(user_id)
                if member:
                    await member.kick(reason='Kick komutu ile atıldı.')
                    await ctx.send(f'{user.name}#{user.discriminator} kullanıcısı sunucudan atıldı.')
                else:
                    await ctx.send('Belirtilen kullanıcı bulunamadı.')
            except discord.NotFound:
                await ctx.send('Belirtilen kullanıcı bulunamadı.')
            except discord.Forbidden:
                await ctx.send('Bot, yeterli izne sahip değil. Lütfen botunun "Üyeleri At" iznine sahip olduğundan emin olun.')
        else:
            await ctx.send('Bu komutu kullanma izniniz yok.')

def setup(bot):
    bot.add_cog(Kick(bot))
