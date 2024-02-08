import requests
from discord.ext import commands
from dotenv import load_dotenv
import os

# Çevresel değişkenleri yükle
load_dotenv()

class HavadurumuCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name='havadurumu',
        description='Belirli bir şehrin hava durumunu alır.'
    )
    async def havadurumu_slash(self, ctx, il: str):
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': il,
            'appid': os.getenv('OPENWEATHERMAP_API_KEY'),  # .env dosyanıza eklediğiniz çevresel değişken
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
    bot.add_cog(HavadurumuCog(bot))
