import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from utils.log import FileLogger
from utils.guild_member import get_guild_member_nickname, get_guild_channel_index
import utils.line_manager as line_manager

class ping:
    def __init__(self):
        self.usage = '!ping [人數]'
        self.auth_warning = '你不是這個公會的隊員吧?'
        self.basic = True

    def check_param(self, param):
        if not param:
            return True
        elif len(param[0]) == 1 and param[0][0].isdigit():
            self.base = False
            return True
        else:
            return False

    def check_auth(self, auth):
        user_nickname = get_guild_member_nickname(auth['guild_id'], auth['user_id'])
        if user_nickname:
            return True
        else:
            return False

    def run(self, user_auth, param):
        guild_id = user_auth['guild_id']
        channel_id = user_auth['channel_id']

        offset = 0
        if not self.basic:
            offset = int(param[0])

        boss_id = get_guild_channel_index(guild_id, channel_id)
        players = line_manager.get_line(guild_id, boss_id, offset)

        if players:
            result = ''
            for player in players:
                result += f'<@{player}> '
            return result
        return '目前沒有人在排隊'