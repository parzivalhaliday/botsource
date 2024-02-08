import discord
from discord.ext import commands
from datetime import datetime

class ServerInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="serverinfo", aliases=["serverbilgi"])
    async def server_info(self, ctx, server_id: int = None):
        if server_id is None:
            server = ctx.guild
        else:
            server = self.bot.get_guild(server_id)

        if server is None:
            await ctx.send("Belirtilen ID'ye sahip bir sunucu bulunamadı.")
            return

        embed = discord.Embed(title=f"{server.name} Sunucu Bilgileri", color=0x00ff00)
        embed.add_field(name="ID", value=server.id, inline=False)
        embed.add_field(name="Üyeler", value=server.member_count, inline=False)
        embed.add_field(name="Kanallar", value=len(server.channels), inline=False)
        embed.add_field(name="Roller", value=len(server.roles), inline=False)
        embed.add_field(name="Sunucu Oluşturulma Tarihi", value=self.format_date(server.created_at), inline=False)
        embed.add_field(name="Sunucu Sahibi", value=f"{server.owner.name}#{server.owner.discriminator}", inline=False)

        if server.icon:
            embed.set_thumbnail(url=server.icon.url)

        invite = await self.create_invite_link(server)
        if invite:
            embed.add_field(name="Davet Bağlantısı", value=invite, inline=False)

        # Emoji ekleniyor
        emoji = "➡️"
        embed.add_field(name="Rolleri Görmek İçin Emojiye Tıkla", value=f"Emojiye tıklayarak rolleri görebilirsiniz: {emoji}")

        message = await ctx.send(embed=embed)
        await message.add_reaction(emoji)

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == emoji

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
        except TimeoutError:
            pass
        else:
            role_list = "\n".join([role.mention for role in server.roles])
            await ctx.send(f"Sunucudaki Roller:\n{role_list}")

    async def create_invite_link(self, server):
        try:
            invite = await server.text_channels[0].create_invite(max_age=300, max_uses=1)
            return invite.url
        except Exception as e:
            print(f"Hata: {e}")
            return None

    def format_date(self, date):
        return date.strftime("%Y-%m-%d %H:%M:%S")

def setup(bot):
    bot.add_cog(ServerInfo(bot))
