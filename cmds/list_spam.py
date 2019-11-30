import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from utils.log import FileLogger
from utils.spammer import list_spammer

class list_spam:
    def __init__(self):
        self.usage = '!list_spam [指令]'
        self.auth_warning = ''

    def check_param(self, param):
        return len(param) < 2

    def check_auth(self, auth):
        return True

    def run(self, user_auth, param):
        cmd = ''
        if len(param) == 1:
            cmd = param[0]

        comment = ''
        spam_list = list_spammer(cmd)
        for key in spam_list:
            comment += f'{key} 共{spam_list[key]}種反應\n'

        if not comment:
            comment = '目前沒有設定反應'
        return comment