import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from utils.log import FileLogger
from utils.spammer import clear_spammer

class clear_spam:
    def __init__(self):
        self.usage = '!clear_spam <指令> [old|new]\n指定old將移除最舊的反應，指定new將移除最新的反應\n不指定將移除該指令及所有反應'
        self.auth_warning = '只有公會的管理員才能使用這個功能'
        self.mode = 0

    def check_param(self, param):
        if len(param) == 2:
            if param[1] == 'old':
                self.mode = 1
            elif param[1] == 'new':
                self.mode = -1
            else:
                return False
            return True
        else:
            return len(param) == 1

    def check_auth(self, auth):
        return auth['user_admin']

    def run(self, user_auth, param):
        result = clear_spammer(param[0], self.mode)
        if result:
            return '指令清除成功'
        else:
            return '指令清除失敗'
