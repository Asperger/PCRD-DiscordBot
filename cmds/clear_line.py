import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from utils.log import FileLogger
import utils.line_manager as line_manager

class clear_line:
    def __init__(self):
        self.usage = '!clear_line'

    def run(self, user_auth, *param):
        if param and len(param[0]) != 0:
            return self.usage
        if not user_auth['user_admin']:
            return '只有公會的管理員才能使用這個功能'

        result = line_manager.clear(user_auth['guild_id'])
        if result:
            return '排隊記錄清除成功'
        else:
            return '目前沒有排隊記錄'