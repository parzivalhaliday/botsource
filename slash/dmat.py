import discord
from discord.ext import commands

class DmatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="dmat",
        description="Belirli bir kullanıcıya özel mesaj atar."
    )
    async def dmat_slash(self, ctx,
                         user: discord.User,
                         message: str = ".",
                         count: int = 1):
        for _ in range(count):
            dm_message = f"{user.mention} {message}\n"
            await user.send(dm_message)

def setup(bot):
    bot.add_cog(DmatCog(bot))
