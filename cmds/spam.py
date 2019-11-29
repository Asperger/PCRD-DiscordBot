import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from utils.log import FileLogger
from utils.spammer import get_spammer

class spam:
    def __init__(self):
        self.usage = '!spam <你的指令> 或 !<你的指令>'
        self.auth_warning = ''

    def check_param(self, param):
        return len(param) > 0

    def check_auth(self, auth):
        return True

    def run(self, user_auth, param):
        return get_spammer(param[0])
