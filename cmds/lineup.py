import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from utils.log import FileLogger
from utils.guild_member import get_guild_member_nickname, get_guild_channel_index
import utils.line_manager as line_manager

class lineup:
    def __init__(self):
        self.usage = '!+1'

    def run(self, user_auth, *param):
        guild_id = user_auth['guild_id']
        user_id = user_auth['user_id']
        channel_id = user_auth['channel_id']

        user_nickname = get_guild_member_nickname(guild_id, user_id)
        if not user_nickname:
            return '你不是這個公會的隊員吧?'

        if param and len(param[0]) == 1 and param[0][0] == 'help':
            return self.usage

        boss_id = get_guild_channel_index(guild_id, channel_id)
        result = line_manager.line_up(guild_id, user_id, boss_id)
        if result:
            return f'{user_nickname} 排隊成功'
        else:
            return f'{user_nickname} 排隊失敗'