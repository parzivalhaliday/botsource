import discord
from discord.ext import commands

class YetkiKomutları(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='yetkiler')
    async def get_permissions(self, ctx, user_id: int = None, guild_id: int = None):
        if user_id is None or guild_id is None:
            await ctx.send("Lütfen bir kullanıcı ID'si ve bir sunucu ID'si girin.")
            return

        try:
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                await ctx.send("Belirtilen sunucu ID'ye sahip bir sunucu bulunamadı.")
                return

            member = guild.get_member(user_id)
            if member is None:
                await ctx.send("Belirtilen kullanıcı ID'ye sahip bir üye bulunamadı.")
                return

            # Kullanıcının yetkilerini listele
            user_permissions = [str(permission) for permission in member.guild_permissions]
            await ctx.send(f"{member.display_name} kullanıcısının yetkileri:\n\n{user_permissions}")
        except Exception as e:
            await ctx.send(f"Hata: {e}")

def setup(bot):
    bot.add_cog(YetkiKomutları(bot))
