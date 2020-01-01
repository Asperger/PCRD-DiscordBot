from utils.log import FileLogger
from utils.spammer import rename_spammer

from utils.cmds_registry import register
register(cmd="rename_spam", alias="rename_spam")

class rename_spam:
    def __init__(self):
        self.usage = '!rename_spam <你的指令> <新的指令>'
        self.auth_warning = '只有公會的管理員才能使用這個功能'

    def check_param(self, param):
        return len(param) == 2

    def check_auth(self, auth):
        return auth['user_admin']

    def run(self, user_auth, param):
        result = rename_spammer(param[0], param[1])
        if not result:
            return '嘿嘿'
        else:
            return result