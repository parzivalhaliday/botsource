import discord
from discord.ext import commands
import requests
import os
import json
from dotenv import load_dotenv

# .env dosyasındaki çevresel değişkenleri yükleyin
load_dotenv()

class LolProfil(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='profil')
    async def lol_profil(self, ctx, *, summoner_info):
        try:
            api_key = os.getenv('RIOT_API_KEY')
            region = 'tr1'
            game_version = os.getenv('GAME_VERSION', '13.24.1')  # Varsayılan değeri 13.24.1 olarak belirle

            if "#" not in summoner_info:
                await ctx.send("Lütfen doğru bir Riot ID ve etiket girin.")
                return

            summoner_name, tag_line = summoner_info.split("#", 1)

            # Riot API'den kullanıcı bilgilerini al
            response = requests.get(f'https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}?api_key={api_key}')
            response.raise_for_status()
            summoner_info = response.json()

            # Riot API'den puuid bilgisini al
            puuid_response = requests.get(f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{summoner_info["puuid"]}?api_key={api_key}')
            puuid_response.raise_for_status()
            puuid_info = puuid_response.json()

            # Riot API'den summonerId bilgisini al
            summoner_id = puuid_info['id']
            old_nick = puuid_info['name']


            # Riot API'den rank bilgilerini al
            rank_response = requests.get(f'https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}?api_key={api_key}')
            rank_response.raise_for_status()
            rank_info = rank_response.json()

            # Riot API'den profil resmi bilgisini al
            profile_icon_id = puuid_info.get('profileIconId', 0)

            # Profil resmi CDN URL'sini oluştur
            profile_icon_url = f'https://ddragon.leagueoflegends.com/cdn/{game_version}/img/profileicon/{profile_icon_id}.png'

            # Discord gömülü oluştur
            embed = discord.Embed(title=f"{summoner_info['gameName']}'s Profili", color=0x00ff00)
            embed.set_thumbnail(url=profile_icon_url)
            
            embed.add_field(name="Riot ID", value=f"{summoner_info['gameName']}#{summoner_info['tagLine']}", inline=False)
            embed.add_field(name="Level", value=puuid_info['summonerLevel'], inline=False)

            embed.add_field(name="Oyuncu ID", value= "||" +puuid_info['id'] + "||", inline=False)
            embed.add_field(name="Hesap ID", value= "||"+ puuid_info['accountId'] + "||", inline=False)
            embed.add_field(name="Puuid", value= "||" + puuid_info['puuid'] + "||", inline=False)


            # Rütbe bilgilerini gömülüye ekleyin
            if rank_info:
                for entry in rank_info:
                    queue_type = entry.get('queueType', 'Bilinmeyen Sıra Türü')
                    if queue_type != 'CHERRY':  # CHERRY kuyruğunu kontrol et
                        tier = entry.get('tier', 'Bilinmeyen Rütbe')
                        rank = entry.get('rank', 'Bilinmeyen Kademe')
                        lp = entry.get('leaguePoints', 0)
                        wins = entry.get('wins', 0)
                        losses = entry.get('losses', 0)
                        rank_text = f"{tier} {rank} ({lp} LP)\nWins: {wins} / Losses: {losses}"
                        embed.add_field(name=f"{queue_type} Rütbesi", value=rank_text, inline=False)

            # Şampiyon ustalık bilgilerini gömülüye ekleyin
            mastery_response = requests.get(f'https://{region}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid_info["puuid"]}?api_key={api_key}')
            mastery_response.raise_for_status()
            mastery_info = mastery_response.json()

            # Şampiyon isimlerini yükle
            with open('riot/champion_names.json', 'r') as file:
                champion_names = json.load(file)


            # Top 5 şampiyon ustalık bilgilerini gömülüye ekleyin
            top_5_champions = mastery_info[:5]
            champion_points_text = "\n".join([f"{champion_names[str(champ['championId'])]}: {champ['championPoints']} puan" for champ in top_5_champions])
            embed.add_field(name="Top 5 Şampiyon Ustalığı", value=champion_points_text, inline=False)
            embed.add_field(name="Eski Nick",value=old_nick,inline=False)

            # Discord'a gömülüyü gönder
            await ctx.send(embed=embed)

        except requests.exceptions.HTTPError as errh:
            print("HTTP Error:", errh)
            await ctx.send(f'Böyle bi oyuncu yok')

        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            await ctx.send(f'Hata: Bağlantı Hatası')

        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            await ctx.send(f'Hata: Timeout')

        except requests.exceptions.RequestException as err:
            print("Oops, something went wrong:", err)
            await ctx.send(f'Hata:')

def setup(bot):
    bot.add_cog(LolProfil(bot))
