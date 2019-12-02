import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from utils.log import FileLogger
from utils.spammer import set_spammer_weight

class set_spam_weight:
    def __init__(self):
        self.usage = '!set_spam_weight <你的指令> [w1 w2 w3 ...]'
        self.auth_warning = '只有公會的管理員才能使用這個功能'

    def check_param(self, param):
        return len(param) > 1 and all(map(lambda v : v.isdigit(), param[1:]))

    def check_auth(self, auth):
        return auth['user_admin']

    def run(self, user_auth, param):
        weight = [int(v) for v in param[1:]]
        result = set_spammer_weight(param[0], weight)
        if result:
            return f'{param[0]} 權重設定成功'
        else:
            return f'{param[0]} 權重設定失敗'