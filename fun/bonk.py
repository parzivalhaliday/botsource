import discord
from discord.ext import commands
from PIL import Image
from io import BytesIO
import requests

class BonkCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="bonk", description="bonk")
    async def bonk(self, ctx, member1: discord.Member, member2: discord.Member):
        # İlk üyenin avatarını alın
        avatar1_url = member1.avatar.url

        # İkinci üyenin avatarını alın
        avatar2_url = member2.avatar.url

        # Bonk resmini yükleyin
        bonk_image = Image.open("fun/bonk.png")

        # İlk üyenin avatarını indirin ve boyutlandırın
        avatar1 = Image.open(requests.get(avatar1_url, stream=True).raw)
        avatar1 = avatar1.resize((90, 90))

        # İkinci üyenin avatarını indirin ve boyutlandırın
        avatar2 = Image.open(requests.get(avatar2_url, stream=True).raw)
        avatar2 = avatar2.resize((80, 80))

        # Avatarları resmin üzerine ekleyin
        bonk_image.paste(avatar1, (65, 20))
        bonk_image.paste(avatar2, (360, 100))

        # Sonucu gönderin
        with BytesIO() as image_binary:
            bonk_image.save(image_binary, 'PNG')
            image_binary.seek(0)
            await ctx.send(file=discord.File(fp=image_binary, filename='bonked.png'))

def setup(bot):
    bot.add_cog(BonkCog(bot))
