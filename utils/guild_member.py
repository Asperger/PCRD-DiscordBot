from time import time
from utils.timer import timer_member_list, timer_channel_list
from utils.log import FileLogger

_guild_member_list = {}
_guild_channel_list = {}

def setup_guild_member_list(guild):
    global timer_member_list
    if guild.id in _guild_member_list:
        elapsed_time = time() - timer_member_list[guild.id]
        if elapsed_time < 86400:
            return
    _guild_member_list[guild.id] = {}
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
            _guild_member_list[guild.id][guild.members[i].id] = nick
        elif display_name:
            _guild_member_list[guild.id][guild.members[i].id] = display_name
        else:
            _guild_member_list[guild.id][guild.members[i].id] = guild.members[i].name
    timer_member_list[guild.id] = time()

def get_guild_member_nickname(guild_id, user_id):
    if guild_id not in _guild_member_list:
        FileLogger.warn('Unknown guild id')
        return

    if user_id not in _guild_member_list[guild_id]:
        FileLogger.warn('Unknown user id')
        return

    return _guild_member_list[guild_id][user_id]

def get_guild_member_list(guild_id):
    if guild_id not in _guild_member_list:
        FileLogger.warn('Unknown guild id')
        return
    return set(_guild_member_list[guild_id].keys())

def setup_guild_channel_list(guild):
    if guild.id in _guild_channel_list:
        elapsed_time = time() - timer_channel_list[guild.id]
        if elapsed_time < 86400:
            return
    _guild_channel_list[guild.id] = {}
    for channel in guild.channels:
        if channel.type.name == 'text' and channel.category.name.endswith('討論區'):
            if channel.name.startswith('一王-'):
                _guild_channel_list[guild.id][1] = channel.id
                _guild_channel_list[guild.id][channel.id] = 1
            elif channel.name.startswith('二王-'):
                _guild_channel_list[guild.id][2] = channel.id
                _guild_channel_list[guild.id][channel.id] = 2
            elif channel.name.startswith('三王-'):
                _guild_channel_list[guild.id][3] = channel.id
                _guild_channel_list[guild.id][channel.id] = 3
            elif channel.name.startswith('四王-'):
                _guild_channel_list[guild.id][4] = channel.id
                _guild_channel_list[guild.id][channel.id] = 4
            elif channel.name.startswith('五王-'):
                _guild_channel_list[guild.id][5] = channel.id
                _guild_channel_list[guild.id][channel.id] = 5
    timer_channel_list[guild.id] = time()

def get_guild_channel_list(guild_id):
    if guild_id not in _guild_channel_list:
        FileLogger.warn('Unknown guild id')
        return
    return _guild_channel_list[guild_id]

def get_guild_channel_index(guild_id, channel_id):
    if guild_id not in _guild_channel_list:
        FileLogger.warn('Unknown guild id')
        return
    if channel_id not in _guild_channel_list[guild_id]:
        FileLogger.warn('Unknown channel id')
        return
    return _guild_channel_list[guild_id][channel_id]

def get_guild_channel_id(guild_id, boss_index):
    if guild_id not in _guild_channel_list:
        FileLogger.warn('Unknown guild id')
        return
    if boss_index not in _guild_channel_list[guild_id]:
        FileLogger.warn('Unknown boss index')
        return
    return _guild_channel_list[guild_id][boss_index]
