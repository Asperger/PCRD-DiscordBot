# Work with Python 3.6
import dbl
import discord
from discord.ext import commands

import asyncio
import logging
logging.basicConfig(format='%(asctime)s %(message)s')

from utils.token import get_token
import args

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author.bot:
        return

    if message.content.startswith('!'):
        msg = args.parse_args(message.content[1:])
        await message.channel.send(msg)

@client.event
async def on_ready():
    print('Logged in as '+client.user.name+'('+str(client.user.id)+')')
    logging.info('Logged in as '+client.user.name+'('+str(client.user.id)+')')

client.run(get_token())
