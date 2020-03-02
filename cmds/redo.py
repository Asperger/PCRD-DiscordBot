from utils.db import sqlur
from utils.google_sheets_utils import redo as sheets_redo
from utils.guild_member import get_guild_member_nickname

from utils.cmds_registry import register
register(cmd="redo", alias="redo")

class redo:
    def __init__(self):
        self.usage = '!redo'
        self.auth_warning = '你不是這個公會的隊員吧?'

    def check_param(self, param):
        return not param

    def check_auth(self, auth):
        user_nickname = get_guild_member_nickname(auth['user_id'])
        if user_nickname:
            return True
        else:
            return False

    def run(self, user_auth, param):
        try:
            description = sqlur.redo()
            sheets_redo()
        except Exception:
            return '沒有可以重做的紀錄'
        return f'已重做 {description}'