# bot.py
import os

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from dotenv import load_dotenv
import json
from re import search
import requests

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    # activity = discord.Game(name="to Lore", type=2)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Magic"))


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hello, {member.name}, welcome traveller!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if search("^/sheet", message.content):
        print("TOAST")


client.run(TOKEN)
