import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
import datetime
import asyncio

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

version = "0.1"

@bot.event
async def on_ready():
    print('Pouleto is ready!')
    channel = bot.get_channel('972811106580058132')
    now = datetime.datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    embed=discord.Embed(title=f"{bot.user.name} is ready !", description=f"Up date: {dt_string},\n\nVersion: {version},\n{bot.user.name} by Rog#8698.", color=0x6BFF33)
    await channel_connected.send(embed=embed)
    print(f"{bot.user.name} is ready.")  
    synced = await bot.tree.sync()
    print(f"Synced {synced} commands.")

bot.run('MTA2NTkzOTk1MTY5NjQ5MDU4Nw.GHURt3.oVh5rpiJFs5cMLLDwlb9o16pABYrtmpzd53JPM')