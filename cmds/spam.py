from utils.log import FileLogger
from utils.spammer import get_spammer

from utils.cmds_registry import register
register(cmd="spam", alias="spam")

class spam:
    def __init__(self):
        self.usage = '!spam <你的指令> 或 !<你的指令>'
        self.auth_warning = ''

    def check_param(self, param):
        return len(param) > 0

    def check_auth(self, auth):
        return True

    def run(self, user_auth, param):
        return get_spammer(param[0])[0]
