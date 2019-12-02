import utils.db
import utils.google_sheets_utils
from utils.guild_member import get_guild_member_nickname

from utils.cmds_registry import register
register(cmd="undo", alias="undo")

class undo:
    def __init__(self):
        self.usage = '!undo'
        self.auth_warning = '你不是這個公會的隊員吧?'

    def check_param(self, param):
        return not param

    def check_auth(self, auth):
        user_nickname = get_guild_member_nickname(auth['guild_id'], auth['user_id'])
        if user_nickname:
            return True
        else:
            return False

    def run(self, user_auth, param):
        try:
            description = utils.db.sqlur.undo()
            utils.google_sheets_utils.undo()
        except Exception:
            return '沒有可以取消的紀錄'
        return f'已取消 {description}'