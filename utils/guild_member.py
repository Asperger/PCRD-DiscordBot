import time
import utils.timer
from utils.log import FileLogger

guild_member_list = {}

def setup_guild_member_list(guild):
    if guild.id in guild_member_list:
        elapsed_time = time.time() - utils.timer.timer_member_list[guild.id]
        if elapsed_time < 86400:
            return
    guild_member_list[guild.id] = {}
    for i in range(0, len(guild.members)):
        if '隊員' not in guild.members[i].roles:
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