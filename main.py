# Work with Python 3.6
import dbl
import discord
from discord.ext import commands
import json
import collections
import asyncio
from utils.log import FileLogger

from utils.token import get_token
from args import parse_args, usage

from utils.guild_member import setup_guild_member_list, setup_guild_channel_list

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
        setup_guild_channel_list(message.author.guild)
        setup_guild_member_list(message.author.guild)
        user_auth = {
            'guild_id': message.author.guild.id,
            'user_id': message.author.id,
            'user_admin': message.author.guild_permissions.administrator,
            'channel_id': message.channel.id
        }
        msg = parse_args(user_auth, message.content[1:])
        if msg:
            if isinstance(msg, collections.Mapping):
                # it's a dict
                for key in msg:
                    await message.channel.send(f'{key}: {json.dumps(msg[key], sort_keys=True, indent=2, ensure_ascii=False)}')
            elif isinstance(msg, list):
                # it's a list
                for i in range(len(msg)):
                    await message.channel.send(msg[i])
            else:
                await message.channel.send(msg)

@client.event
async def on_member_join(member):
    if not member.bot:
        for channel in member.guild.channels:
            if channel.name == '公會大廳':
                await channel.send(f':grinning: 請等會長將你加入"隊員"身分組，再嘗試使用以下功能:\n{usage()}')

@client.event
async def on_ready():
    FileLogger.info(f'Logged in as {client.user.name}({client.user.id})')
    for guild in client.guilds:
        setup_guild_channel_list(guild)

client.run(get_token())