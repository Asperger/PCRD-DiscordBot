import utils.db
from utils.guild_member import get_guild_member_nickname

class undo:
    def __init__(self):
        self.usage = '!undo'
    def run(self, guild_id, user_id, *param):
        if param and len(param[0]) > 0:
            return self.usage
        user_nickname = get_guild_member_nickname(guild_id, user_id)
        if not user_nickname:
            return '你不是這個公會的隊員吧?'
        try:
            description = utils.db.sqlur.undo()
        except Exception:
            return '沒有可以取消的紀錄'
        return f'已取消 {description}'