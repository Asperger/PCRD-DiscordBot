import utils.db

class undo:
    def __init__(self):
        self.usage = '!undo'
    def run(self, guild_id, user_id, *param):
        if param and len(param[0]) > 0:
            return self.usage
        try:
            utils.db.sqlur.undo()
        except Exception:
            return '沒有可以取消的紀錄'
        return '已取消'