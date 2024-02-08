import requests
import datetime
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# .env dosyasındaki çevresel değişkenleri yükleyin
load_dotenv()

class SteamProfile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="steam", description="steam profile")
    async def steam(self, ctx, steam_id):
        # Steam Web API'nin URL'si
        api_url = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={os.getenv("STEAM_API_KEY")}&steamids={steam_id}'

        try:
            # API'ye istek gönder
            response = requests.get(api_url)

            # İstek başarılı mı kontrol et
            if response.status_code == 200:
                data = response.json()

                # Kullanıcı bilgilerini al
                player_info = data.get('response', {}).get('players', [{}])[0]
                steam_username = player_info.get('personaname', 'Bilinmiyor')
                avatar_url = player_info.get('avatarfull', 'Bilinmiyor')
                last_logoff_timestamp = player_info.get('lastlogoff', 0)
                time_created_timestamp = player_info.get('timecreated', 0)

                # Unix zaman damgalarını tarihe çevir
                last_logoff_datetime = datetime.datetime.utcfromtimestamp(
                    last_logoff_timestamp)

                # Hesap oluşturma tarihini kontrol et
                if time_created_timestamp == 0:
                    time_created = 'Bilinmiyor'
                else:
                    time_created_datetime = datetime.datetime.utcfromtimestamp(
                        time_created_timestamp)
                    time_created = time_created_datetime.strftime('%Y-%m-%d %H:%M:%S')

                today = datetime.datetime.utcnow()

                # Bugünkü tarihin bir gün öncesini al
                days_since_last_logoff = (today - last_logoff_datetime).days

                # Steam Web API'ye istek gönder
                steam_api_url = f'http://api.steampowered.com/IPlayerService/GetSteamLevel/v1/?key={os.getenv("STEAM_API_KEY")}&steamid={steam_id}'
                steam_response = requests.get(steam_api_url)

                # Steam seviyesini al
                steam_data = steam_response.json()
                steam_level = steam_data.get('response', {}).get('player_level',
                                                                'Bilinmiyor')

                # Embed oluştur
                embed = discord.Embed(title=f'Steam Profili - {steam_username}',
                                      color=0x7289DA)
                embed.set_thumbnail(url=avatar_url)
                embed.add_field(name='Steam ID', value=steam_id, inline=False)
                embed.add_field(name='Steam Kullanıcı Adı',
                                value=steam_username,
                                inline=False)
                embed.add_field(name='Son Giriş Tarihi',
                                value=f'{days_since_last_logoff} gün önce',
                                inline=False)
                embed.add_field(name='Hesap Oluşturulma Tarihi',
                                value=time_created,
                                inline=False)
                embed.add_field(name='Steam Seviyesi', value=steam_level, inline=False)

                # Sonucu Discord'a gönder
                await ctx.send(embed=embed)
            else:
                await ctx.send('API isteği başarısız oldu.')

        except Exception as e:
            await ctx.send(f'Hata oluştu: {str(e)}')

def setup(bot):
    bot.add_cog(SteamProfile(bot))