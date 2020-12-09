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
    "sheet": "test166",
    "image": ""
}, {
    "player": "Connor",
    "id": 251488731750465536,
    "sheet": "porterham729",
    "image": "https://cdn.discordapp.com/attachments/253712269882425344/786059458690285598/Porter_Hamelin.png"
}, {
    "player": "Anna",
    "id": 271372320604553216,
    "sheet": "talkidres809",
    "image": "https://cdn.discordapp.com/attachments/271377218192670721/786263500971311125/PSX_20201209_100304.jpg"
}, {
    "player": "Randy",
    "id": 317721524251394051,
    "sheet": "",
    "image": ""
}, {
    "player": "Wesley",
    "id": 270331940870160384,
    "sheet": "",
    "image": ""
}, {
    "player": "Leticia",
    "id": 533511368385495081,
    "sheet": "",
    "image": ""
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

    mention = False
    mentions = message.mentions
    if len(mentions) > 0:
        mention = True
        mentioned = mentions[0].id
        print("Mentioned:", mentions[0].name)
    else:
        mentioned = message.author.id

    inDataBase = False
    i = 0
    for i in range(len(players)):
        if players[i]['id'] == mentioned:
            player = players[i]
            if player['sheet'] != '':
                inDataBase = True
        i = (i + 1)


    if inDataBase == True:
        url = "https://openlegend.heromuster.com/api/character/" + player['sheet']
        payload = {}
        files = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload, files=files)
        data = response.json()
        char = data['success']['character']
        print(char)

        # Start Embed
        embed = discord.Embed(title=char['charactername'], colour=discord.Colour(0x436d1a),
                              description=char['description'])
        embed.set_author(name=char['playername'],
                         url=("https://openlegend.heromuster.com/character?s=" + data['success']['characterid']),
                         icon_url="https://openlegend.heromuster.com/character-sheet-icon.png")

        if (len(players[1]['image']) > 0):
            embed.set_thumbnail(url=player['image'])

        if (search("^/perk", message.content) or search("^/flaw", message.content)) and inDataBase:
            # perks and flaws
            perk = False
            perks = []
            if char['perk1'] != '':
                perk = True
                perks.append(char['perk1'])
            if char['perk2'] != '':
                perk = True
                perks.append(char['perk2'])

            if perks:
                embed.add_field(name="Perks", value=perks, inline=True)

            flaw = False
            flaws = []
            if char['flaw1'] != '':
                flaw = True
                flaws.append(char['flaw1'])
            if char['flaw2'] != '':
                flaw = True
                flaws.append(char['flaw2'])

            if flaws:
                embed.add_field(name="Flaw", value=flaws, inline=True)
            await message.channel.send(embed=embed)

        if search("^/sheet", message.content) and inDataBase:
            embed.add_field(name="HP", value=char['hp'], inline=True)
            embed.add_field(name="WL", value=("¥"+char['wealth']+"k"), inline=True)
            embed.add_field(name="Level", value=(char['level'] + " (" + char['xp'] + ")"), inline=True)

            embed.add_field(name="Guard", value=char['evasion'], inline=True)
            embed.add_field(name="Toughness", value=char['toughness'], inline=True)
            embed.add_field(name="Resolve", value=char['resolve'], inline=True)

            embed.add_field(name="Initiative", value=char['initiative'], inline=True)
            if not (char['agility'] == '0' or char['agility'] == ''):
                embed.add_field(name="Agility", value=char['agility'], inline=True)
            if not (char['fortitude'] == '0' or char['fortitude'] == ''):
                embed.add_field(name="Fortitude", value=char['fortitude'], inline=True)
            if not (char['might'] == '0' or char['might'] == ''):
                embed.add_field(name="Might", value=char['might'], inline=True)
            if not (char['learning'] == '0' or char['learning'] == ''):
                embed.add_field(name="Learning", value=char['learning'], inline=True)
            if not (char['logic'] == '0' or char['logic'] == ''):
                embed.add_field(name="Logic", value=char['logic'], inline=True)
            if not (char['perception'] == '0' or char['perception'] == ''):
                embed.add_field(name="Perception", value=char['perception'], inline=True)
            if not (char['will'] == '0' or char['will'] == ''):
                embed.add_field(name="Will", value=char['will'], inline=True)
            if not (char['deception'] == '0' or char['deception'] == ''):
                embed.add_field(name="Deception", value=char['deception'], inline=True)
            if not (char['persuasion'] == '0' or char['persuasion'] == ''):
                embed.add_field(name="Persuasion", value=char['persuasion'], inline=True)
            if not (char['presence'] == '0' or char['presence'] == ''):
                embed.add_field(name="Presence", value=char['presence'], inline=True)
            if not (char['alteration'] == '0' or char['alteration'] == ''):
                embed.add_field(name="Alteration", value=char['alteration'], inline=True)
            if not (char['energy'] == '0' or char['energy'] == ''):
                embed.add_field(name="Energy", value=char['energy'], inline=True)
            if not (char['entropy'] == '0' or char['entropy'] == ''):
                embed.add_field(name="Entropy", value=char['entropy'], inline=True)
            if not (char['influence'] == '0' or char['influence'] == ''):
                embed.add_field(name="Influence", value=char['influence'], inline=True)
            if not (char['movement'] == '0' or char['movement'] == ''):
                embed.add_field(name="Movement", value=char['movement'], inline=True)
            if not (char['prescience'] == '0' or char['prescience'] == ''):
                embed.add_field(name="Prescience", value=char['prescience'], inline=True)
            if not (char['protection'] == '0' or char['protection'] == ''):
                embed.add_field(name="Protection", value=char['protection'], inline=True)
            # embed.add_field(name="Attribute Points", value=(char['attrspent'] + "/" + char['attrtotal']), inline=True)
            # embed.add_field(name="Feat Points", value=(char['featspent'] + "/" + char['feattotal']), inline=True)

            await message.channel.send(embed=embed)
    else:
        await message.channel.send("No sheet was found.")


client.run(TOKEN)
