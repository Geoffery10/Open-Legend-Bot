# bot.py
import os

import discord
import requests
from dotenv import load_dotenv
import json
from re import search
import requests

players = [{
    "player": "Geoffery",
    "id": 253710834553847808,
    "sheet": "test166"
}, {
    "player": "Connor",
    "id": 251488731750465536,
    "sheet": "porterham729",
    "image": "https://cdn.discordapp.com/attachments/253712269882425344/786059458690285598/Porter_Hamelin.png"
}]

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

    # curl --location --request GET '{{domain}}/character/{{characterid}}'
    if search("^/sheet", message.content):
        url = "https://openlegend.heromuster.com/api/character/porterham729"

        payload = {}
        files = {}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload, files=files)

        # print(response.text.encode('utf8'))
        data = response.json()
        character = data['success']['character']
        # await message.channel.send(data)


client.run(TOKEN)
