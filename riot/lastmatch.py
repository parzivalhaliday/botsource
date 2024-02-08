import discord
from discord.ext import commands
import requests
import os

class LastMatch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='lastmatch')
    async def last_match(self, ctx, *, summoner_info):
        try:
            api_key = os.getenv('RIOT_API_KEY')
            region = 'europe'

            if "#" not in summoner_info:
                await ctx.send("Lütfen doğru bir Riot ID ve etiket girin.")
                return

            summoner_name, tag_line = summoner_info.split("#", 1)

            response = requests.get(f'https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}?api_key={api_key}')
            response.raise_for_status()
            summoner_data = response.json()

            if 'puuid' not in summoner_data:
                await ctx.send("Oyuncu bilgileri alınamadı. Lütfen doğru bir Riot ID ve etiket girin.")
                return

            puuid = summoner_data['puuid']

            count = 10  # Sabit olarak 10 maç alınacak

            url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}&api_key={api_key}'
            response = requests.get(url)
            response.raise_for_status()

            match_ids = response.json()

            embed = discord.Embed(title="Son Maçlar", description=f"Son {count} maçın detayları:", color=0x00ff00)

            for match_id in match_ids:
                match_url = f'https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}'
                match_response = requests.get(match_url)
                match_data = match_response.json()

                for participant in match_data.get('info', {}).get('participants', []):
                    if participant.get('puuid') == puuid:
                        champion_name = participant.get('championName', 'Bilinmiyor')
                        kills = participant.get('kills', 'Bilinmiyor')
                        deaths = participant.get('deaths', 'Bilinmiyor')
                        assists = participant.get('assists', 'Bilinmiyor')

                        embed.add_field(name=f"Maç ID: {match_id}", value=f"Champion: {champion_name}\nKills: {kills}\nDeaths: {deaths}\nAssists: {assists}\n-------------------", inline=False)

            # Döngü bittiğinde mesajı gönder
            await ctx.send(embed=embed)

        except Exception as e:
            print(f"Hata: {e}")
            await ctx.send(f'Hata: {e}')

def setup(bot):
    bot.add_cog(LastMatch(bot))
