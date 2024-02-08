import discord
from discord.ext import commands
from discord.ext.commands import Paginator
import requests
import os
import json

class TopMastery10(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv('RIOT_API_KEY')  # Riot API anahtarınızı çevresel değişkenden alın
        self.region = 'europe'
        self.champions_per_page = 10
        self.champion_data = self.load_champion_data()

    def load_champion_data(self):
        try:
            with open('riot/champion_names.json', 'r') as file:
                champion_data = json.load(file)
                return champion_data
        except FileNotFoundError:
            print("Hata: champion_names.json dosyası bulunamadı.")
            return {}

    @commands.command(name='top10')
    async def top_mastery(self, ctx, *, summoner_info):
        try:
            # Giriş kontrolü
            if "#" not in summoner_info:
                await ctx.send("Lütfen doğru bir Riot ID ve etiket girin.")
                return

            summoner_name, tag_line = summoner_info.split("#", 1)

            # Kullanıcıya ait puuid bilgisini çek
            summoner_response = requests.get(f'https://{self.region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}?api_key={self.api_key}')
            summoner_response.raise_for_status()
            summoner_info = summoner_response.json()
            puuid = summoner_info['puuid']

            # Şampiyon mastery bilgilerini çek
            mastery_response = requests.get(f'https://tr1.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-puuid/{puuid}?api_key={self.api_key}')
            mastery_response.raise_for_status()
            mastery_info = mastery_response.json()

            # Şampiyonları puanlarına göre sırala
            sorted_champions = sorted(mastery_info, key=lambda x: x['championPoints'], reverse=True)

            # Sayfalama yap
            pages = Paginator(prefix='```', suffix='```', max_size=2000)
            for index, champion in enumerate(sorted_champions, start=1):
                champion_name = self.champion_data.get(str(champion['championId']),)
                champion_points = champion['championPoints']

                if index % self.champions_per_page == 0:
                    pages.add_line(f"{index}. {champion_name}: {champion_points} Şampiyon Puanı")
                    pages.close_page()
                else:
                    pages.add_line(f"{index}. {champion_name}: {champion_points} Şampiyon Puanı")

            # İlk sayfayı gönder
            message = await ctx.send(pages.pages[0])

            # İleri ve geri tepkilerini ekle
            await message.add_reaction('◀️')
            await message.add_reaction('▶️')

            def check(reaction, user):
                return user == ctx.message.author and reaction.message.id == message.id

            page = 0
            while True:
                try:
                    reaction, _ = await self.bot.wait_for('reaction_add', timeout=60.0, check=check)

                    if reaction.emoji == '▶️' and page < len(pages.pages) - 1:
                        page += 1
                    elif reaction.emoji == '◀️' and page > 0:
                        page -= 1

                    await message.edit(content=pages.pages[page])

                    # Kullanıcının tepkisini sil
                    await message.remove_reaction(reaction.emoji, ctx.message.author)

                except TimeoutError:
                    break

        except requests.exceptions.HTTPError as errh:
            print("HTTP Error:", errh)
            await ctx.send(f'böyle bi oyuncu yok')

        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            await ctx.send(f'Hata: Bağlantı Hatası - ')

        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            await ctx.send(f'Hata: Timeout - ')

        except requests.exceptions.RequestException as err:
            print("Oops, something went wrong:", err)
            await ctx.send(f'Hata:')

def setup(bot):
    bot.add_cog(TopMastery10(bot))
