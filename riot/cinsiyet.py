
import discord
from discord.ext import commands
from predict_gender import predict_gender
import json

class Cinsiyet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.champion_data = self.load_champion_data()

    def load_champion_data(self):
        try:
            with open('riot/champion_names.json', 'r') as file:
                champion_data = json.load(file)
                return champion_data
        except FileNotFoundError:
            print("Hata: champion_names.json dosyası bulunamadı.")
            return {}

    @commands.command(name="cinsiyet",
                      aliases=["kizmi", "kızmı"],
                      description="user cinsiyet")
    async def cinsiyet_tahmini(self, ctx, *, summoner_info):
        result = predict_gender(summoner_info, self.champion_data)
        await ctx.send(result)

def setup(bot):
    bot.add_cog(Cinsiyet(bot))
