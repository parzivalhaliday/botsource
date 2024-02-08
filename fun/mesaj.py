from PIL import Image, ImageDraw, ImageFont
import io
import discord
from discord.ext import commands

class ScreenshotCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ss", description="Son mesajın ekran görüntüsünü alır ve gönderir.")
    async def screenshot(self, ctx):
        # Son mesajı al
        last_message = await ctx.channel.history(limit=2).flatten()

        # Eğer son mesajın içinde metin varsa
        if last_message[1].content:
            # Mesajı resme dönüştür ve koordinatlara yerleştir
            image = await self.text_to_image(last_message[1], "fun/justchat.png", (200, 70, 420, 70), (200, 180, 420, 400, 250))

            # Resmi gönder
            await ctx.send(file=discord.File(fp=image, filename='screenshot.png'))
        else:
            await ctx.send("Son mesajda metin bulunamadı.")

    async def text_to_image(self, message, background_path, *coordinates):
        # Arka plan resmi yükle
        background = Image.open(background_path)

        # Bir resim oluştur
        img = Image.new('RGBA', (background.width, background.height), color=(255, 255, 255, 0))
        img.paste(background, (0, 0))

        d = ImageDraw.Draw(img)

        try:
            # Kullanıcı resmini yükle
            avatar = await message.author.avatar.read()
            avatar_image = Image.open(io.BytesIO(avatar)).resize((45, 45))

            # Kullanıcı resmini belirtilen koordinatlara yerleştir
            img.paste(avatar_image, (210, 30))

            # Kullanıcı adını belirtilen koordinatlara yerleştir
            font = ImageFont.load_default()
            user_name = message.author.name
            text = f"{message.content}\n\nYazan: {user_name} - Tarih: {message.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
            d.text((210, 40), text, font=font, fill=(0, 0, 0, 255))

        except IOError as e:
            # Eğer resim yüklenemezse, alternatif bir font kullan
            font = ImageFont.load_default()
            # Mesaj tarihini ve kullanıcı adını resme ekle
            date = message.created_at.strftime("%Y-%m-%d %H:%M:%S")
            text = f"{message.content}\n\nYazan: {message.author.name} - Tarih: {date}"

            # Metni belirtilen koordinatlara yerleştir
            for coord in coordinates:
                d.text(coord[:2], text, font=font, fill=(0, 0, 0, 255))

        # Resmi bir bayt nesnesine çevir
        image_binary = io.BytesIO()
        img.save(image_binary, 'PNG')
        image_binary.seek(0)

        return image_binary

def setup(bot):
    bot.add_cog(ScreenshotCog(bot))
