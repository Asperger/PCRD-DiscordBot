import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from utils.log import FileLogger
from utils.spammer import set_spammer

class set_spam:
    def __init__(self):
        self.usage = '!set_spam <request> <response>'

    def check_param(self, param):
        if len(param) != 2:
            return False
        else:
            return True

    def run(self, user_auth, *param):
        if not self.check_param(param[0]):
            return self.usage

        result = set_spammer(param[0][0], param[0][1])
        if result:
            return '嘿嘿'
        else:
            return '肚子餓了...'
