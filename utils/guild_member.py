from utils.log import FileLogger

guild_member_list = {}

def setup_guild_member_list(guild):
    if guild.id not in guild_member_list:
        guild_member_list[guild.id] = { guild.members[i].id : guild.members[i] for i in range(0, len(guild.members) ) }

def get_guild_member_nickname(guild_id, user_id):
    if guild_id not in guild_member_list:
        FileLogger.warn('Unknown guild id')
        return

    if user_id not in guild_member_list[guild_id]:
        FileLogger.warn('Unknown user id')
        return

    return guild_member_list[guild_id][user_id].nick
