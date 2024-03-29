from utils.db import sqlur
from utils.google_sheets_utils import undo as sheets_undo
from utils.guild_member import check_guild_crew, get_guild_member_nickname, get_guild_channel_board

from utils.cmds_registry import register
register(cmd="undo", alias="undo")

class undo:
    def __init__(self):
        self.usage = '!undo'
        self.auth_warning = '你不是這個公會的隊員吧?'

    def check_param(self, param):
        return not param

    def check_auth(self, auth):
        if auth['channel_id'] != get_guild_channel_board():
            self.auth_warning = '請到登記區登記'
            return False

        return check_guild_crew(auth['user_id'])

    def run(self, user_auth, param):
        try:
            description = sqlur.undo()
            sheets_undo()
        except Exception:
            return '沒有可以取消的紀錄'
        return f'已取消 {description}'