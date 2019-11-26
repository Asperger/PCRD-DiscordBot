import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from utils.log import FileLogger
from utils.guild_member import get_guild_member_nickname, get_guild_channel_index
import utils.line_manager as line_manager

class ping:
    def __init__(self):
        self.usage = '!ping'

    def run(self, user_auth, *param):
        guild_id = user_auth['guild_id']
        user_id = user_auth['user_id']
        channel_id = user_auth['channel_id']

        user_nickname = get_guild_member_nickname(guild_id, user_id)
        if not user_nickname:
            return '你不是這個公會的隊員吧?'
        if param and len(param[0]) > 0:
            return self.usage

        boss_id = get_guild_channel_index(guild_id, channel_id)
        players = line_manager.get_line(guild_id, boss_id)

        if players:
            result = ''
            for player in players:
                result += f'<@{player}> '
            return result
        return '目前沒有人在排隊'