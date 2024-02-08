import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands

class TurkishSuperLig(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tff", aliases=["superlig","sikebahce"], description="TFF Süper Lig takım sıralamasını alır.")
    async def get_turkish_super_lig_teams(self, ctx):
        # Web sayfasını iste ve içeriği al
        url = 'https://www.tff.org/default.aspx?pageID=198'
        response = requests.get(url)

        # Hata kontrolü
        if response.status_code == 200:
            # Sayfa içeriğini BeautifulSoup kullanarak analiz et
            soup = BeautifulSoup(response.text, 'html.parser')

            # Takım isimlerini saklamak için boş bir liste oluştur
            team_names = []

            # <a> etiketlerini seçin ve belirli bir ID deseni ile eşleşenleri filtreleyin
            a_elements = soup.find_all(
                'a',
                id=lambda x: x and x.startswith(
                    'ctl00_MPane_m_198_12490_ctnr_m_198_12490_grvACetvel_ctl'))
            for a in a_elements:
                text = a.get_text(strip=True)
                # "FENERBAHÇE A.Ş." bilgisini "ŞİKEBAHÇE A.Ş." olarak değiştir
                text = text.replace("FENERBAHÇE A.Ş.", "ŞİKEBAHÇE A.Ş.")
                team_names.append(text)

            # Embed oluştur
            embed = discord.Embed(title='Türkiye Süper Lig Takım Sıralaması',
                                  color=0x7289DA)
            team_list = '\n'.join(team_names)
            embed.add_field(name='Takım Sıralaması', value=team_list, inline=False)

            # Embed'i mesaj olarak gönder
            await ctx.send(embed=embed)
        else:
            await ctx.send('Web sayfasına erişilemedi. Hata kodu: ' +
                           str(response.status_code))

def setup(bot):
    bot.add_cog(TurkishSuperLig(bot))
