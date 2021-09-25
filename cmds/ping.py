from utils.log import FileLogger
from utils.guild_member import check_guild_crew, get_guild_member_nickname, get_guild_channel_index
from utils.line_manager import get_line

from utils.cmds_registry import register
register(cmd="ping", alias="ping")

class ping:
    def __init__(self):
        self.usage = '!ping [人數|list]\n不指定人數時將呼叫正選的人\n指定人數時則以此數目呼叫備選的人\nlist將列出排隊中的所有人但不呼叫'
        self.auth_warning = '你不是這個公會的隊員吧?'
        self.offset = 0
        self.list_all = False

    def check_param(self, param):
        if not param:
            return True
        elif len(param) == 1:
            if param[0].isdigit():
                self.offset = int(param[0])
                return True
            elif param[0] == 'list':
                self.list_all = True
                return True
            else:
                return False
        else:
            return False

    def check_auth(self, auth):
        return check_guild_crew(auth['user_id'])

    def run(self, user_auth, param):
        channel_id = user_auth['channel_id']

        boss_id = get_guild_channel_index(channel_id)
        players = get_line(boss_id, self.offset, self.list_all)

        result = ''
        if players:
            if self.list_all:
                for player in players:
                    player_nickname = get_guild_member_nickname(player.id)
                    result += f'{player_nickname} {player.comment}\n'
            else:
                for player in players:
                    result += f'<@{player.id}> {player.comment}\n'
        else:
            result = '目前沒有人在排隊'
        return result