# Work with Python 3.6
import dbl
import discord
from discord.ext import commands

import asyncio
from utils.log import FileLogger

from utils.token import get_token
from args import parse_args

from utils.guild_member import setup_guild_member_list

client = discord.Client()

@client.event
async def on_message(message):
    if message.content == '!stop' and message.author.guild_permissions.administrator:
        await client.logout()
        return

    # we do not want the bot to reply to itself
    if message.author.bot:
        return

    if message.content.startswith('!'):
        setup_guild_member_list(message.author.guild)
        msg = parse_args(message.author.guild.id, message.author.id, message.content[1:])
        if msg:
            await message.channel.send(msg)

@client.event
async def on_ready():
    FileLogger.info(f'Logged in as {client.user.name}({client.user.id})')

client.run(get_token())