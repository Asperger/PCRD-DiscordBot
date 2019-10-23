import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from utils.log import FileLogger
import time
import utils.timer

class usage:
    def __init__(self):
        self.usage = '!help'

    def check_param(self, param):
        if len(param) != 0:
            return False
        else:
            return True

    def run(self, user_auth, *param):
        if not self.check_param(param[0]):
            return self.usage

        elapsed_time = time.time() - utils.timer.timer_usage
        if elapsed_time < 30:
            return '肚子餓了...'
        utils.timer.timer_usage = time.time()
        return '`!fill` 填表\n`!status` 查看出刀情況\n`!undo` 取消上次輸入的內容 ***不限定使用者!!! 你會把別人輸入的紀錄取消掉!!!***\n`!redo` 重新輸入上次取消的內容\n`!help` 重看這篇說明\n在各個指令之後加上 `help` 查看使用格式\n這些指令只能在一部份頻道使用，使用前請注意頻道的成員名單，如果我不在名單上代表這個頻道不能使用這些指令\n如果我不在線上代表我生病了 :cry:'
