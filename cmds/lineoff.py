from utils.log import FileLogger
from utils.guild_member import get_guild_member_nickname, get_guild_channel_index
import utils.line_manager as line_manager

class lineoff:
    def __init__(self):
        self.usage = '!-1 [備註]\n備註沒有作用，你可以隨便寫或不寫，例如你要用的隊伍或一些幹話'
        self.auth_warning = '你不是這個公會的隊員吧?'

    def check_param(self, param):
        return True

    def check_auth(self, auth):
        user_nickname = get_guild_member_nickname(auth['guild_id'], auth['user_id'])
        if user_nickname:
            return True
        else:
            return False

    def run(self, user_auth, param):
        guild_id = user_auth['guild_id']
        user_id = user_auth['user_id']
        channel_id = user_auth['channel_id']

        user_nickname = get_guild_member_nickname(guild_id, user_id)

        boss_id = get_guild_channel_index(guild_id, channel_id)
        result = line_manager.line_off(guild_id, user_id, boss_id)
        if result:
            return f'{user_nickname} 取消排隊成功'
        else:
            return f'{user_nickname} 取消排隊失敗'