# Work with Python 3.6
import dbl
import discord
from discord.ext import commands

import asyncio
from utils.log import FileLogger

from utils.token import get_token
import args

client = discord.Client()

@client.event
async def on_message(message):
    if message.content == '!stop' and message.author.id == 538023210864738314:
        await client.logout()
        return

    # we do not want the bot to reply to itself
    if message.author.bot:
        return

    if message.content.startswith('!'):
        msg = args.parse_args(message.author.id, message.content[1:])
        if msg:
            await message.channel.send(msg)

@client.event
async def on_ready():
    FileLogger.info('Logged in as '+client.user.name+'('+str(client.user.id)+')')

client.run(get_token())
