import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from utils.log import FileLogger
from utils.spammer import clear_spammer

class clear_spam:
    def __init__(self):
        self.usage = '!clear_spam <request>'
        self.auth_warning = '只有公會的管理員才能使用這個功能'

    def check_param(self, param):
        return len(param) == 1

    def check_auth(self, auth):
        return auth['user_admin']

    def run(self, user_auth, param):
        result = clear_spammer(param[0])
        if result:
            return '指令清除成功'
        else:
            return '指令清除失敗'
