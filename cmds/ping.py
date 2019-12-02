from utils.log import FileLogger
from utils.guild_member import get_guild_member_nickname, get_guild_channel_index
import utils.line_manager as lm

from utils.cmds_registry import register
register(cmd="ping", alias="ping")

class ping:
    def __init__(self):
        self.usage = '!ping [人數]\n不指定人數時將呼叫正選的人\n指定人數時則以此數目呼叫備選的人'
        self.auth_warning = '你不是這個公會的隊員吧?'
        self.basic = True

    def check_param(self, param):
        if not param:
            return True
        elif len(param) == 1 and param[0].isdigit():
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
        players = lm.get_line(guild_id, boss_id, offset)

        result = ''
        if players:
            for player in players:
                result += f'<@{player}> '
        else:
            result = '目前沒有人在排隊'
        return result