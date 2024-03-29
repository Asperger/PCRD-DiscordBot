from time import time
from utils.timer import timer_member, timer_channel
from utils.log import FileLogger

_guild_crew_list = set()
_guild_member_list = {}
_guild_channel_list = {}
_guild_channel_board = 0

def setup_guild_member_list(guild, override=False):
    global timer_member, _guild_member_list, _guild_crew_list
    if bool(_guild_member_list) :
        elapsed_time = time() - timer_member
        if elapsed_time < 86400 and not override:
            return

    FileLogger.info(f'Setting up members in {guild.name}')
    _guild_crew_list = set()
    _guild_member_list = {}
    for i in range(0, len(guild.members)):
        valid = False
        for role in guild.members[i].roles:
            if role.name == '隊員':
                valid = True
                break
        if valid:
            _guild_crew_list.add(guild.members[i].id)

        nick = guild.members[i].nick
        display_name = guild.members[i].display_name
        if nick:
            _guild_member_list[guild.members[i].id] = nick
        elif display_name:
            _guild_member_list[guild.members[i].id] = display_name
        else:
            _guild_member_list[guild.members[i].id] = guild.members[i].name
    timer_member = time()

def check_guild_crew(user_id):
    return user_id in _guild_crew_list

def get_guild_member_nickname(user_id):
    if user_id not in _guild_member_list:
        FileLogger.warn('Unknown user id')
        return
    return _guild_member_list[user_id]

def get_guild_member_list():
    return set(_guild_member_list.keys())

def setup_guild_channel_list(guild, override=False):
    global timer_channel, _guild_channel_list, _guild_channel_board
    if bool(_guild_channel_list):
        elapsed_time = time() - timer_channel
        if elapsed_time < 86400 and not override:
            return

    FileLogger.info(f'Setting up channels in {guild.name}')
    _guild_channel_list = {}
    for channel in guild.channels:
        if channel.type.name == 'text' and channel.category.name.endswith('公會戰討論區'):
            if channel.name.startswith('一王'):
                _guild_channel_list[1] = channel.id
                _guild_channel_list[channel.id] = 1
            elif channel.name.startswith('二王'):
                _guild_channel_list[2] = channel.id
                _guild_channel_list[channel.id] = 2
            elif channel.name.startswith('三王'):
                _guild_channel_list[3] = channel.id
                _guild_channel_list[channel.id] = 3
            elif channel.name.startswith('四王'):
                _guild_channel_list[4] = channel.id
                _guild_channel_list[channel.id] = 4
            elif channel.name.startswith('五王'):
                _guild_channel_list[5] = channel.id
                _guild_channel_list[channel.id] = 5
        if channel.type.name == 'text' and channel.name.endswith('刀傷登記區'):
            _guild_channel_board = channel.id
    timer_channel = time()

def get_guild_channel_list():
    return _guild_channel_list

def get_guild_channel_index(channel_id):
    if channel_id not in _guild_channel_list:
        FileLogger.warn('Unknown channel id')
        return
    return _guild_channel_list[channel_id]

def get_guild_channel_id(boss_index):
    if boss_index not in _guild_channel_list:
        FileLogger.warn('Unknown boss index')
        return
    return _guild_channel_list[boss_index]

def get_guild_channel_board():
    return _guild_channel_board