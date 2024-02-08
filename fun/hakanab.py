import requests
from bs4 import BeautifulSoup
import re
from discord.ext import commands

class HakocScrape(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hakoc')
    async def scrape(self, ctx):
        url = "https://wot-widget-wargaming.streamtools.io/revanch/1223"

        # Web sayfasını çek
        response = requests.get(url)

        # İçeriği kontrol et ve parse et
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # JavaScript kodunu içeren etiketi bul
            script_tag = soup.find('script', string=lambda text: "updateCounter" in str(text))

            if script_tag:
                # JavaScript kodunu içeriği al
                script_content = script_tag.string

                # Sayısal değeri regex ile bul
                match = re.search(r'updateCounter\((\d+)\);', script_content)
                if match:
                    counter_value = match.group(1)
                    await ctx.send(f"hakoç abiden alacağım 70 tl sayısı {counter_value} ")
                else:
                    await ctx.send("Sayısal değer bulunamadı.")
            else:
                await ctx.send("Belirtilen JavaScript kodu bulunamadı.")
        else:
            await ctx.send(f"Sayfa çekme hatası: {response.status_code}")

def setup(bot):
    bot.add_cog(HakocScrape(bot))
