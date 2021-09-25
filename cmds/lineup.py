from utils.log import FileLogger
from utils.guild_member import check_guild_crew, get_guild_member_nickname, get_guild_channel_index
from utils.line_manager import line_up

from utils.cmds_registry import register
register(cmd="lineup", alias="+1")

class lineup:
    def __init__(self):
        self.usage = '!+1 [備註]\n備註沒有作用，你可以隨便寫或不寫，例如你要用的隊伍或一些幹話'
        self.auth_warning = '你不是這個公會的隊員吧?'

    def check_param(self, param):
        return True

    def check_auth(self, auth):
        return check_guild_crew(auth['user_id'])

    def run(self, user_auth, param):
        user_id = user_auth['user_id']
        channel_id = user_auth['channel_id']

        user_nickname = get_guild_member_nickname(user_id)

        comment = ' '.join(param) if param else ''
        boss_id = get_guild_channel_index(channel_id)
        result = line_up(user_id, boss_id, comment)
        if result:
            return f'{user_nickname} {result}'
        else:
            return '隊伍設定錯誤'