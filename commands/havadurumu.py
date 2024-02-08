import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv
import os

load_dotenv()

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='havadurumu')
    async def havadurumu(self, ctx, il: str = None):
        weatherapi_key = os.getenv('OPENWEATHERMAP_API_KEY')

        if il and il.lower() == 'erzulüm':
            il = 'Erzurum'

        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': il,
            'appid': weatherapi_key,
            'units': 'metric',  # Derece Celsius ile sıcaklık almak için
        }

        # API'den hava durumu verilerini alın
        response = requests.get(base_url, params=params)
        weather_data = response.json()

        if weather_data["cod"] == 200:
            # Hava durumu verilerini çıkartın
            temperature = weather_data["main"]["temp"]

            # Sonucu kullanıcıya gönderin
            await ctx.send(f'{il}: Sıcaklığı: {temperature} °C')
        else:
            await ctx.send(f'{il} için hava durumu bilgisi bulunamadı.')

def setup(bot):
    bot.add_cog(Weather(bot))
