# Work with Python 3.6
from discord import Client, User, Embed, Intents
from json import dumps
from collections import Mapping
from urllib.parse import urlparse

from utils.log import FileLogger
from utils.token import get_token
from args import parse_args
from cmds.usage import usage_content

from utils.guild_member import setup_guild_member_list, setup_guild_channel_list
from utils.func_registry import execute

intent = Intents(messages=True, guilds=True, members=True)
client = Client(intents=intent)

def is_url(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False

def embed_template(user:User) -> Embed:
    embed = Embed(color=0xffa200)
    embed.set_author(name=user.display_name, icon_url=user.avatar_url)
    embed.set_footer(text=client.user.name, icon_url=client.user.avatar_url)
    return embed

def get_embed(user:User, content:dict) -> Embed:
    embed = embed_template(user)
    if "title" in content:
        embed.title = content["title"]
    if "description" in content:
        embed.description = content["description"]
    for key in content:
        if key not in ("title", "description"):
            embed.add_field(name=key, value=content[key], inline=False)
    return embed

@client.event
async def on_message_edit(before, after):
    if before.content != after.content:
        await on_message(after)

@client.event
async def on_message(message):
    if message.content == '!stop' and message.author.guild_permissions.administrator:
        FileLogger.info('User requested shutdown')
        execute()
        await client.logout()
        return

    # we do not want the bot to reply to itself
    if message.author.bot:
        return

    if message.content.startswith('!') or message.content.startswith('！'):
        setup_guild_channel_list(message.author.guild)
        setup_guild_member_list(message.author.guild)

        user_auth = {
            'guild_id': message.author.guild.id,
            'user_id': message.author.id,
            'user_admin': message.author.guild_permissions.administrator,
            'channel_id': message.channel.id
        }

        content = message.content[1:]
        if message.attachments:
            content += f' {message.attachments[0].url}'
        msg = parse_args(user_auth, content)
        if msg:
            if isinstance(msg, Mapping):
                # it's a dict
                embed = get_embed(message.author, msg)
                await message.channel.send(embed=embed)
            elif isinstance(msg, list):
                # it's a list
                embed = embed_template(message.author)
                for i in range(len(msg)):
                    embed.add_field(name=i, value=msg[i], inline=False)
                await message.channel.send(embed=embed)
            elif is_url(msg):
                # it's an url
                embed = Embed(color=0xffa200)
                embed.set_image(url=msg)
                await message.channel.send(embed=embed)
            else:
                await message.channel.send(msg)

@client.event
async def on_member_join(member):
    if not member.bot:
        embed = get_embed(member, usage_content)
        embed.description += f'\n:grinning: 請等會長將你加入"隊員"身分組，再嘗試使用以下功能:'
        await member.send(embed=embed)

@client.event
async def on_ready():
    FileLogger.info(f'Logged in as {client.user.name}({client.user.id})')
    for guild in client.guilds:
        setup_guild_channel_list(guild)

client.run(get_token())