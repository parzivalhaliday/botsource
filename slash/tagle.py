import discord
from discord.ext import commands

class TagleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="tagle",
        description="Belirli bir kullanıcıyı etiketleyerek mesaj gönderir."
    )
    async def tagle_slash(self, ctx, user: discord.User, count: int, message: str = "."):
        for _ in range(count):
            await ctx.send(f"{user.mention} {message}")

def setup(bot):
    bot.add_cog(TagleCog(bot))
