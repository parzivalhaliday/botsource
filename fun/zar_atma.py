import discord
from discord.ext import commands
import random

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='zarat', aliases=['zar_at', 'zar'])
    async def zar_atma(self, ctx, *oyuncular: discord.Member):
        if len(oyuncular) < 2:
            await ctx.send("Oyun için en az 2 oyuncu gerekiyor!")
            return

        zarlar = {oyuncu: random.randint(1, 6) for oyuncu in oyuncular}
        
        kazanan = max(zarlar, key=zarlar.get)
        kazanan_zar = zarlar[kazanan]

        embed = discord.Embed(title="Zar Atma Sonuçları", color=0x00ff00)
        embed.add_field(name="Oyuncular", value=", ".join([oyuncu.mention for oyuncu in oyuncular]), inline=False)
        embed.add_field(name="Zarlar", value=", ".join([f'{oyuncu.mention}: {zar}' for oyuncu, zar in zarlar.items()]), inline=False)
        embed.add_field(name="Kazanan", value=f"{kazanan.mention} with {kazanan_zar} zar!", inline=False)

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))
