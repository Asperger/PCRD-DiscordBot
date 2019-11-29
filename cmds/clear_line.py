import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from utils.log import FileLogger
import utils.line_manager as lm

class clear_line:
    def __init__(self):
        self.usage = '!clear_line [幾王]\n不指定王將清除所有排隊紀錄'
        self.auth_warning = '只有公會的管理員才能使用這個功能'
        self.boss = 0

    def check_param(self, param):
        result = True
        if not param:
            pass
        elif len(param) == 1 and param[0].isdigit():
            b = int(param[0])
            if b > 0 and b < 6:
                self.boss = b
            else:
                result = False
        else:
            result = False
        return result

    def check_auth(self, auth):
        return auth['user_admin']

    def run(self, user_auth, *param):
        comment = '設定失敗'
        result = lm.clear_line(user_auth['guild_id'], self.boss)
        if result:
            if self.boss == 0:
                comment = '排隊記錄清除成功'
            else:
                comment = f'{self.boss}王 排隊記錄清除成功'
        return comment