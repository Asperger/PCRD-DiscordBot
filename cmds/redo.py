import utils.db

class redo:
    def __init__(self):
        self.usage = '!redo'
    def run(self, guild_id, user_id, *param):
        if param and len(param[0]) > 0:
            return self.usage
        try:
            utils.db.sqlur.redo()
        except Exception:
            return '沒有可以重做的紀錄'
        return '已重做'