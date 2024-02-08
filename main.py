import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv  
from statuses import statuses  
from onmessage import on_message_handler
import keep_alive


load_dotenv()  # .env dosyasını yükleyin


intents = discord.Intents.all()

bot = commands.Bot(command_prefix=['!', 'lan '],
                   intents=intents,
                   case_insensitive=True)

@tasks.loop(seconds=60)
async def change_status():
    status = statuses[change_status.current_index]
    await bot.change_presence(activity=discord.Game(name=status), status=discord.Status.online)
    change_status.current_index = (change_status.current_index + 1) % len(statuses)

change_status.current_index = 0

@bot.event
async def on_ready():
    print(f'{bot.user.name} hayatta')
    change_status.start()

@bot.command()
async def kapat(ctx):
    await ctx.send('Kapatılıyor...')
    await bot.close()

@bot.command(name='komutlar')
async def list_commands(ctx):
    command_list = [f"!{command.name}" for command in bot.commands]
    await ctx.send("\n".join(command_list))


@bot.event
async def on_message(message):
    await on_message_handler(bot, message)

@bot.command(name='reload', description='Yüklenen komutları yeniden yükler.')
@commands.is_owner()
async def reload(ctx):
    load_commands()
    await ctx.send('Komutlar yeniden yüklendi!')

def is_extension_loaded(bot, extension_name):
    return extension_name in bot.extensions

def load_commands():
    for folder in os.listdir('./'):
        if os.path.isdir(folder) and not folder.startswith('__'):
            for filename in os.listdir(f'./{folder}'):
                if filename.endswith('.py') and filename != 'main.py':
                    extension_name = f'{folder}.{filename[:-3]}'
                    if not is_extension_loaded(bot, extension_name):
                        bot.load_extension(extension_name)
                    else:
                        print(f"Extension '{extension_name}' already loaded")

for folder in os.listdir('./'):
    if os.path.isdir(folder) and not folder.startswith('__'):
        for filename in os.listdir(f'./{folder}'):
            if filename.endswith('.py'):
                bot.load_extension(f'{folder}.{filename[:-3]}')

# Botu çalıştırma
load_commands()
bot.run(os.getenv('DISCORD_TOKEN'))
