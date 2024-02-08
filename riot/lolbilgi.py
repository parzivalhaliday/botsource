import discord
from discord.ext import commands
import requests
import os

class LolBilgi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='lolbilgi')
    async def lol_bilgi(self, ctx, *, summoner_info):
        try:
            api_key = os.getenv('RIOT_API_KEY')  # Riot API anahtarınızı çevresel değişkenden alın
            region = 'europe'

            # Giriş kontrolü
            if "#" not in summoner_info:
                await ctx.send("Lütfen doğru bir Riot ID ve etiket girin.")
                return

            summoner_name, tag_line = summoner_info.split("#", 1)

            # Riot API'den kullanıcı bilgilerini al
            response = requests.get(f'https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}?api_key={api_key}')
            response.raise_for_status()
            summoner_info = response.json()

            # Discord gömülü oluştur
            embed = discord.Embed(title=f"{summoner_info['gameName']}'s Bilgileri", color=0x00ff00)
            embed.add_field(name="puuid", value=summoner_info['puuid'], inline=True)
            embed.add_field(name="gameName", value=summoner_info['gameName'], inline=True)
            embed.add_field(name="tagLine", value=summoner_info['tagLine'], inline=True)

            # Discord'a gömülüyü gönder
            await ctx.send(embed=embed)

        except requests.exceptions.HTTPError as errh:
            print("HTTP Error:", errh)
            await ctx.send(f'Hata: HTTP Error - {errh}')

        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            await ctx.send(f'Hata: Bağlantı Hatası - {errc}')

        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            await ctx.send(f'Hata: Timeout - {errt}')

        except requests.exceptions.RequestException as err:
            print("Oops, something went wrong:", err)
            await ctx.send(f'Hata: {err}')

def setup(bot):
    bot.add_cog(LolBilgi(bot))
