import discord
from discord.ext import commands

class Unban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='unban', help='Belirtilen kullanıcının yasağını kaldırır. Kullanım: !unban <user_id>')
    async def unban(self, ctx, user_id: int):
        # Sadece yetkililerin kullanabileceği bir komut
        if ctx.author.guild_permissions.ban_members:
            try:
                user = await self.bot.fetch_user(user_id)
                await ctx.guild.unban(user)
                await ctx.send(f'{user.name}#{user.discriminator} kullanıcısının yasağı kaldırıldı.')
            except discord.NotFound:
                await ctx.send('Belirtilen kullanıcı bulunamadı.')
            except discord.Forbidden:
                await ctx.send('Bot, yeterli izne sahip değil. Lütfen botunun "Üyeleri Yasakla" iznine sahip olduğundan emin olun.')
        else:
            await ctx.send('Bu komutu kullanma izniniz yok.')

def setup(bot):
    bot.add_cog(Unban(bot))
