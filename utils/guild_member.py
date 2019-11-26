import time
import utils.timer
from utils.log import FileLogger

guild_member_list = {}
guild_channel_list = {}

def setup_guild_member_list(guild):
    if guild.id in guild_member_list:
        elapsed_time = time.time() - utils.timer.timer_member_list[guild.id]
        if elapsed_time < 86400:
            return
    guild_member_list[guild.id] = {}
    for i in range(0, len(guild.members)):
        valid = False
        for role in guild.members[i].roles:
            if role.name == '隊員':
                valid = True
                break
        if not valid:
            continue

        nick = guild.members[i].nick
        display_name = guild.members[i].display_name
        if nick:
            guild_member_list[guild.id][guild.members[i].id] = nick
        elif display_name:
            guild_member_list[guild.id][guild.members[i].id] = display_name
        else:
            guild_member_list[guild.id][guild.members[i].id] = guild.members[i].name
    utils.timer.timer_member_list[guild.id] = time.time()

def get_guild_member_nickname(guild_id, user_id):
    if guild_id not in guild_member_list:
        FileLogger.warn('Unknown guild id')
        return

    if user_id not in guild_member_list[guild_id]:
        FileLogger.warn('Unknown user id')
        return

    return guild_member_list[guild_id][user_id]

def get_guild_member_list(guild_id):
    if guild_id not in guild_member_list:
        FileLogger.warn('Unknown guild id')
        return
    return set(guild_member_list[guild_id].keys())

def setup_guild_channel_list(guild):
    guild_channel_list[guild.id] = {}
    for channel in guild.channels:
        if channel.type.name == 'text' and channel.category.name.endswith('討論區'):
            if channel.name.startswith('一王-'):
                guild_channel_list[guild.id][1] = channel.id
                guild_channel_list[guild.id][channel.id] = 1
            elif channel.name.startswith('二王-'):
                guild_channel_list[guild.id][2] = channel.id
                guild_channel_list[guild.id][channel.id] = 2
            elif channel.name.startswith('三王-'):
                guild_channel_list[guild.id][3] = channel.id
                guild_channel_list[guild.id][channel.id] = 3
            elif channel.name.startswith('四王-'):
                guild_channel_list[guild.id][4] = channel.id
                guild_channel_list[guild.id][channel.id] = 4
            elif channel.name.startswith('五王-'):
                guild_channel_list[guild.id][5] = channel.id
                guild_channel_list[guild.id][channel.id] = 5

def get_guild_channel_list(guild_id):
    if guild_id not in guild_channel_list:
        FileLogger.warn('Unknown guild id')
        return
    return guild_channel_list[guild_id]

def get_guild_channel_index(guild_id, channel_id):
    if guild_id not in guild_channel_list:
        FileLogger.warn('Unknown guild id')
        return
    if channel_id not in guild_channel_list[guild_id]:
        FileLogger.warn('Unknown channel id')
        return
    return guild_channel_list[guild_id][channel_id]

def get_guild_channel_id(guild_id, boss_index):
    if guild_id not in guild_channel_list:
        FileLogger.warn('Unknown guild id')
        return
    if boss_index not in guild_channel_list[guild_id]:
        FileLogger.warn('Unknown boss index')
        return
    return guild_channel_list[guild_id][boss_index]