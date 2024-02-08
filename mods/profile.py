import discord
from discord.ext import commands

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='userinfo', aliases=['ui', 'user'])
    async def user_info(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        roles = [role.mention for role in member.roles if role.name != '@everyone']

        embed = discord.Embed(title=f'Kullanıcı Bilgisi - {member.name}', color=member.color)
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name='Adı', value=member.name, inline=True)
        embed.add_field(name='Takma Adı', value=member.nick, inline=True)
        embed.add_field(name='ID', value=member.id, inline=True)
        embed.add_field(name='Durumu', value=str(member.status).title(), inline=True)
        embed.add_field(name='Oluşturulma Tarihi', value=member.created_at.strftime('%d-%m-%Y %H:%M:%S'), inline=True)
        embed.add_field(name='Sunucuya Katılma Tarihi', value=member.joined_at.strftime('%d-%m-%Y %H:%M:%S'), inline=True)
        embed.add_field(name=f'Roller ({len(roles)})', value=', '.join(roles) if roles else 'Yok', inline=False)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(UserInfo(bot))
