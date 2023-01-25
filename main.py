import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
import datetime
import asyncio
import sqlite3

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

version = "0.1"

async def db_link(name_db):
    conn = sqlite3.connect(name_db)
    c = conn.cursor()
    return c, conn

async def db_get(name_db, table, column, value, get):
    db, base = await db_link(name_db)
    db.execute(f"SELECT {get} FROM {table} WHERE {column} = '{value}'")
    return db.fetchall()

async def message_sender(channel, message):
    await channel.send(message)

@bot.event
async def on_ready():
    now = datetime.datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    synced = await bot.tree.sync()
    print(f"Synced {synced} commands.")
    db, base = await db_link('Pouleto.db')
    print('Database connected.')
    print(f"{bot.user.name} is ready.")  
    channel_connected = bot.get_channel(972811106580058132)
    embed=discord.Embed(title=f"{bot.user.name} is ready !", description=f"Up date: {dt_string},\n\nVersion: {version},\n{bot.user.name} by Le_Poulet#3166.", color=0x69ff33)
    await channel_connected.send(embed=embed)

@bot.tree.command(name="add_alliances", description="Add a new alliance in the database.")
async def add_alliances(interaction: discord.Interaction, alliance: str, channel: str):
    await interaction.response.defer(ephemeral=True)
    if interaction.user.name == "Rog" or interaction.user.name == "Le_Poulet":
        db, base = await db_link('Pouleto.db')
        db.execute(f"INSERT INTO Alliances (Name, Channel) VALUES ('{alliance}', '{channel}')")
        base.commit()
        await interaction.followup.send(f"{alliance} has been added to the database.")
    else:
        await interaction.followup.send("You don't have the permission to do this.")

@bot.tree.command(name="add", description="Add a new player in a alliance.")
async def add(interaction: discord.Interaction, discord_pseudo_and_tags: str, minecraft_pseudo: str, alliance: str):
    await interaction.response.defer(ephemeral=True)
    db, base = await db_link('Pouleto.db')
    Alliance = await db_get('Pouleto.db', 'Alliances', 'Name', alliance, 'Id')
    if Alliance == []:
        await interaction.followup.send(f"{alliance} doesn't exist.")
    else:
        db.execute(f"INSERT INTO Players (Discord, Minecraft, Alliance) VALUES ('{discord_pseudo_and_tags}','{minecraft_pseudo}', '{Alliance[0][0]}')")
        base.commit()
        await interaction.followup.send(f"{discord_pseudo_and_tags.split('#')[0]} has been added to {alliance}.")
        channel = await db_get('Pouleto.db', 'Alliances', 'Name', alliance, 'Channel')
        channel = bot.get_channel(int(channel[0][0]))
        await channel.purge(limit=1)
        message = f"Liste des membres de l'alliance {alliance} :\n\n"
        members = await db_get('Pouleto.db', 'Players', 'Alliance', Alliance[0][0], 'Minecraft')
        for member in members:
            message += f"   - {member[0]}\n"
        await message_sender(channel, message)

@bot.tree.command(name="remove", description="Remove a player from a alliance.")
async def remove(interaction: discord.Interaction, discord_pseudo_and_tags: str, alliance: str):
    await interaction.response.defer(ephemeral=True)
    db, base = await db_link('Pouleto.db')
    Alliance = await db_get('Pouleto.db', 'Alliances', 'Name', alliance, 'Id')
    if Alliance == []:
        await interaction.followup.send(f"{alliance} doesn't exist.")
    else:
        db.execute(f"DELETE FROM Players WHERE Discord = '{discord_pseudo_and_tags}' AND Alliance = '{Alliance[0][0]}'")
        base.commit()
        await interaction.followup.send(f"{discord_pseudo_and_tags.split('#')[0]} has been removed from {alliance}.")
        channel = await db_get('Pouleto.db', 'Alliances', 'Name', alliance, 'Channel')
        channel = bot.get_channel(channel[0][0])
        await channel.purge(limit=1)
        message = f"Liste des membres de l'alliance {alliance} :\n\n"
        members = await db_get('Pouleto.db', 'Players', 'Alliance', Alliance[0][0], 'Minecraft')
        for member in members:
            message += f"   - {member[0]}\n"
        await message_sender(channel, message)
    
@bot.tree.command(name="db", description="Show the database.")
@app_commands.choices(parameters=[Choice(name="alliance", value="alliance"), Choice(name="Players", value="Players")])
async def db(interaction: discord.Interaction, parameters: str):
    await interaction.response.defer(ephemeral=True)
    if interaction.user.name == "Rog":
        if parameters == "alliance":
            db = await db_link('Pouleto.db')
            db.execute("SELECT * FROM Alliances")
            embed=discord.Embed(title="Alliance", color=0x6BFF33)
            for row in db.fetchall():
                embed.add_field(name=row[0], value=row[1], inline=False)
            await interaction.followup.send(embed=embed)
        elif parameters == "Players":
            db = await db_link('Pouleto.db')
            db.execute("SELECT * FROM Players")
            embed=discord.Embed(title="Players", color=0x6BFF33)
            for row in db.fetchall():
                embed.add_field(name=row[0], value=row[1], inline=False)
            await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send("You don't have the permission to do this.")

@bot.tree.command(name="help", description="List all commands or info about a specific command.")
@app_commands.choices(parameters=[
    Choice(name="all", value="all"),
    Choice(name="info", value="info")
])
async def help(interaction: discord.Interaction, parameters: str):
    await interaction.response.defer(ephemeral=True)
    if parameters == "all":
        embed=discord.Embed(title="All commands", description="List of all commands.", color=0x6BFF33)
        embed.add_field(name="!help", value="List all commands or info about a specific command.", inline=False)
        embed.add_field(name="!info", value="Info about the bot.", inline=False)
        embed.add_field(name="!ping", value="Ping the bot.", inline=False)
        embed.add_field(name="!test", value="Test the bot.", inline=False)
        await interaction.followup.send(embed=embed)
    elif parameters == "info":
        embed=discord.Embed(title="Info", color=0x6BFF33)
        embed.add_field(name="!info", value="Info about the bot.", inline=False)
        await interaction.followup.send(embed=embed)

bot.run('MTA2NTkzOTk1MTY5NjQ5MDU4Nw.GSoUhU.YrlyLfW6am3By1VRiKkbQX6YyRBkFkrXxiZfvE')