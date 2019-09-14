import utils.db
import utils.google_sheets_utils
from utils.guild_member import get_guild_member_nickname

class redo:
    def __init__(self):
        self.usage = '!redo'
    def run(self, guild_id, user_id, *param):
        if param and len(param[0]) > 0:
            return self.usage
        user_nickname = get_guild_member_nickname(guild_id, user_id)
        if not user_nickname:
            return '你不是這個公會的隊員吧?'
        try:
            description = utils.db.sqlur.redo()
            utils.google_sheets_utils.redo()
        except Exception:
            return '沒有可以重做的紀錄'
        return f'已重做 {description}'