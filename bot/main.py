import discord
import os
import io
import aiohttp
import requests

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$search card '):
        name = message.content.split('$search card ')[1]
        card = requests.get('https://api.scryfall.com/cards/named?fuzzy='+name).json()

        async with aiohttp.ClientSession() as session:
            async with session.get(card['image_uris']['large']) as resp:
                if resp.status != 200:
                    return await message.channel.send('Could not get the card information, maybe you wrote the name wrong?')
                data = io.BytesIO(await resp.read())
                await message.channel.send(file=discord.File(data, 'card.png'))

        await message.channel.send(card['name'] + ' ' + card['mana_cost'])
        await message.channel.send(card['type_line'])
        await message.channel.send(card['oracle_text'])
        if 'Planeswalker' in card['type_line']:
            await message.channel.send('Loyalty: ' + card['loyalty'])
        if 'Creature' in card['type_line']:
            await message.channel.send('Power/Toughness: ' + card['power'] + '/' + card['toughness'])

client.run(os.environ['DISCORD_TOKEN'])