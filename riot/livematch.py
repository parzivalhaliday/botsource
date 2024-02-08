import requests
import os
import discord
from discord.ext import commands
import json


with open('riot/champion_names.json', 'r') as f:
    champion_names = json.load(f)


class LiveMatch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='livematch')
    async def live_match(self, ctx, *, summoner_info):
        try:
            api_key = os.getenv('RIOT_API_KEY')
            region = 'europe'

            if "#" not in summoner_info:
                await ctx.send("Lütfen doğru bir Riot ID ve etiket girin. Örnek: `!livematch parzi#7340`")
                return

            summoner_name, tag_line = summoner_info.split("#", 1)

            account_url = f'https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}?api_key={api_key}'
            response = requests.get(account_url)
            response.raise_for_status()
            account_data = response.json()
            puuid = account_data['puuid']

            summoner_url = f'https://tr1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}?api_key={api_key}'
            response = requests.get(summoner_url)
            response.raise_for_status()
            summoner_data = response.json()
            summoner_id = summoner_data['id']

            # Aktif maç bilgileri
            active_game_url = f'https://tr1.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{summoner_id}?api_key={api_key}'
            response = requests.get(active_game_url)

            if response.status_code == 404:
                await ctx.send("Oyuncu şu anda bir oyun oynamıyor.")
                return

            response.raise_for_status()
            game_data = response.json()
            embed = discord.Embed(title="Canlı Maç Bilgileri", description=f"{summoner_name} şu anda oynuyor:", color=0x00ff00)

            blue_team = []
            red_team = []
            game_mode = game_data.get('gameMode', 'Bilinmiyor')
            game_type = game_data.get('gameType', 'Bilinmiyor')
            

            for participant in game_data.get('participants', []):
                champion_id = participant.get('championId', None)
                champion_name = champion_names.get(str(champion_id), 'Bilinmiyor')
                summoner_name = participant.get('summonerName', 'Bilinmiyor')
                team_id = participant.get('teamId', 100)  # Mavi takım için 100, Kırmızı takım için 200

                if team_id == 100:
                    blue_team.append(f"**{summoner_name}** \n\n{champion_name}")
                elif team_id == 200:
                    red_team.append(f"**{summoner_name}** \n\n{champion_name}")

            embed.add_field(name="Mavi Takım", value="\n\n".join(blue_team), inline=True)
            embed.add_field(name="Kırmızı Takım", value="\n\n".join(red_team), inline=True)
            embed.add_field(name=" ", value="\u200b", inline=True)

            embed.add_field(name="Mod", value=game_mode, inline=True)

            await ctx.send(embed=embed)

        except Exception as e:
            print(f"Hata: {e}")
            await ctx.send(f'Hata: {e}')

def setup(bot):
    bot.add_cog(LiveMatch(bot))
