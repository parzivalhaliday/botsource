import discord
from discord.ext import commands

class StickerList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sticker", aliases=["stickers"])
    async def list_stickers(self, ctx, guild_id: int = None):
        if guild_id is None:
            await ctx.send("Lütfen bir sunucu ID'si belirtin.")
            return

        try:
            guild = await self.bot.fetch_guild(guild_id)
            if guild:
                stickers = guild.stickers
                if stickers:
                    sticker_list = "\n".join([f"{sticker.name}: {sticker}" for sticker in stickers])
                    await ctx.send(f"Sunucudaki Sticker'lar:\n{sticker_list}")
                else:
                    await ctx.send("Sunucuda sticker bulunmuyor.")
            else:
                await ctx.send("Belirtilen sunucu bulunamadı.")
        except discord.errors.NotFound:
            await ctx.send("Sunucu bulunamadı veya bot sunucuya katılmamış.")

def setup(bot):
    bot.add_cog(StickerList(bot))
