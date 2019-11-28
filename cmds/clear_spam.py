import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from utils.log import FileLogger
from utils.spammer import clear_spammer

class clear_spam:
    def __init__(self):
        self.usage = '!clear_spam <request>'

    def check_param(self, param):
        if len(param) != 1:
            return False
        else:
            return True

    def run(self, user_auth, *param):
        if not self.check_param(param[0]):
            return self.usage

        result = clear_spammer(param[0][0])
        if result:
            return '指令清除成功'
        else:
            return '指令清除失敗'
