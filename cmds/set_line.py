import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from utils.log import FileLogger
import utils.line_manager as line_manager

class set_line:
    def __init__(self):
        self.usage = '!set_line <幾王> <幾刀>\n刀數為0代表不限人數'

    def run(self, user_auth, *param):
        if param and len(param[0]) != 2:
            return self.usage
        if not user_auth['user_admin']:
            return '只有公會的管理員才能使用這個功能'

        boss_id = int(param[0][0])
        amount = int(param[0][1])
        result = line_manager.set_line(user_auth['guild_id'], boss_id, amount)
        if result:
            if amount < 1:
                return f'已重設 {boss_id}王:'
            else:
                return f'已設定 {boss_id}王: {amount}刀'
        else:
            return f'設定失敗'