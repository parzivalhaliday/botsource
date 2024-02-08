import requests
from datetime import datetime, timedelta
from discord.ext import commands
import os

class WeatherCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='havadurumu5gun')
    async def havadurumu5gun(self, ctx, il: str):
        weatherapi_key = os.getenv('OPENWEATHERMAP_API_KEY')

        # Sabah ve akşam saatlerini belirle
        sabah_saati = 12  # Sabah saat 12:00
        aksam_saati = 21  # Akşam saat 21:00
        
        if il and il.lower() == 'erzulüm':
            il = 'Erzurum'
        # Hava durumu API'sine istek gönder
        base_url = "http://api.openweathermap.org/data/2.5/forecast"
        params = {
            'q': il,
            'appid': weatherapi_key,
            'units': 'metric',
        }
        response = requests.get(base_url, params=params)
        weather_data = response.json()

        if weather_data["cod"] == "200":
            # Şehrin zaman dilimini bul
            offset = weather_data["city"]["timezone"]

            # Bugünkü tarihi al
            today = datetime.utcnow()

            # Türkçe gün adları
            gun_adlari = {
                "Monday": "Pazartesi",
                "Tuesday": "Salı",
                "Wednesday": "Çarşamba",
                "Thursday": "Perşembe",
                "Friday": "Cuma",
                "Saturday": "Cumartesi",
                "Sunday": "Pazar",
            }

            # Sonraki 5 günün sabah ve akşam sıcaklıklarını bul
            forecast = weather_data["list"]
            weather_info = {}

            for entry in forecast:
                timestamp = entry["dt"]
                forecast_time = datetime.utcfromtimestamp(timestamp + offset)

                # Sadece sabah ve akşam saatleri için işlem yap
                if forecast_time.hour == sabah_saati or forecast_time.hour == aksam_saati:
                    key = gun_adlari.get(forecast_time.strftime("%A"), "Bilinmiyor")
                    if key not in weather_info:
                        weather_info[key] = {}
                    if forecast_time.hour == sabah_saati:
                        weather_info[key]["sabah"] = entry["main"]["temp"]
                    else:
                        weather_info[key]["aksam"] = entry["main"]["temp"]

            # Mesajı oluştur
            message = f"{il} Hava Durumu:\n"
            for day, temps in weather_info.items():
                sabah_sicaklik = temps.get("sabah", "Bilinmiyor")
                aksam_sicaklik = temps.get("aksam", "Bilinmiyor")
                message += f"{day} Sabah: {sabah_sicaklik} °C, Akşam: {aksam_sicaklik} °C\n"

            # Sonucu Discord'a gönder
            await ctx.send(message)
        else:
            await ctx.send(f'{il} için hava durumu bilgisi bulunamadı.')

def setup(bot):
    bot.add_cog(WeatherCog(bot))
