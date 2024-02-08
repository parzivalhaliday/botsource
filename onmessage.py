# onmessage.py
import discord
from discord.ext import commands
import re

async def on_message_handler(bot, message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel):  
        target_channel_id = 1173087296027893852  
        target_channel = bot.get_channel(target_channel_id)

        if target_channel:
            embed = discord.Embed(
                title="Yeni DM Mesaj",
                description=f"**Gönderen:** {message.author.mention}\n\n{message.content}",
                color=0x7289DA)
            await target_channel.send(embed=embed)

    if "parzi" in message.content.lower():
        emoji_list = [(1079583282284478546, 'bubenaq')]
        for emoji_id, emoji_name in emoji_list:
            emoji = discord.utils.get(bot.emojis, id=emoji_id)
            if emoji:
                await message.add_reaction(emoji)

    # 🍪
    if "enma" in message.content.lower():
        emoji_list = [
            (1152049328169422868, 'Thresh'),
            (1152049414920228915, 'Seraphine'),
            (1152049441700843600, 'Soraka')
        ]
        for emoji_id, emoji_name in emoji_list:
            emoji = discord.utils.get(bot.emojis, id=emoji_id)
            if emoji:
                await message.add_reaction(emoji)

    if "<@811169601491566592>" in message.content.lower():
        emojis = ["🗑", "Rakan:1152049375409872948", "🪝"]
        for emoji in emojis:
            await message.add_reaction(emoji)

    if "pine" in message.content.lower():
        emojis = ["🗑", "Rakan:1152049375409872948", "🪝"]
        for emoji in emojis:
            await message.add_reaction(emoji)

    if "günaydın" in message.content.lower():
        await message.add_reaction("☀️")

    if message.content.lower() == "knauc":
        await message.add_reaction("✋")
        await message.add_reaction("🐶")
        await message.add_reaction("🤚")

    if "cya" in message.content.lower():
        emojis = ["🚶‍♀️", "cyabic:1172264939709288560", "🚶‍♂️"]
        for emoji in emojis:
            await message.add_reaction(emoji)

    twitter_url_pattern = r'https://twitter\.com/\S+'
    twitter_urls = re.findall(twitter_url_pattern, message.content)

    if twitter_urls:
        for url in twitter_urls:
            modified_url = url.replace('https://twitter.com/', 'https://fxtwitter.com/')
            await message.delete()
            await message.channel.send(f"{message.author.mention}  \n{modified_url}")

    instagram_url_pattern = r'https://instagram\.com/\S+'
    instagramr_urls = re.findall(instagram_url_pattern, message.content)

    if instagramr_urls:
        for url in instagramr_urls:
            modified_url = url.replace('https://instagram.com/', 'https://ddinstagram.com/')
            await message.delete()
            await message.channel.send(f"{message.author.mention}  \n{modified_url}")

    wwwtwitter_url_pattern = r'https://www.twitter\.com/\S+'
    wwwtwitter_urls = re.findall(wwwtwitter_url_pattern, message.content)

    if wwwtwitter_urls:
        for url in wwwtwitter_urls:
            modified_url = url.replace('https://www.twitter.com/', 'https://fxtwitter.com/')
            await message.delete()
            await message.channel.send(f"{message.author.mention}  \n{modified_url}")

    wwwinstagram_url_pattern = r'https://www.instagram\.com/\S+'
    wwwinstagramr_urls = re.findall(wwwinstagram_url_pattern, message.content)

    if wwwinstagramr_urls:
        for url in wwwinstagramr_urls:
            modified_url = url.replace('https://www.instagram.com/', 'https://ddinstagram.com/')
            await message.delete()
            await message.channel.send(f"{message.author.mention}  \n{modified_url}")
    else:
        await bot.process_commands(message)
