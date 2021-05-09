from utils.log import FileLogger
from utils.spammer import clear_spammer, get_spammer

from utils.cmds_registry import register
register(cmd="clear_spam", alias="clear_spam")
register(cmd="clear_spam", alias="cs")

class clear_spam:
    def __init__(self):
        self.usage = '!clear_spam <指令> [編號]\n指定編號將移除該反應\n不指定將移除該指令及所有反應'
        self.auth_warning = '只有公會的管理員或作者才能使用這個功能'
        self.request = ""
        self.order = -1

    def check_param(self, param):
        if len(param) > 0:
            self.request = param[0]

        if len(param) == 2:
            if param[1].isdigit():
                self.order = int(param[1])
                return True
            else:
                return False
        else:
            return len(param) == 1

    def check_auth(self, auth):
        author = get_spammer(self.request, self.order)[1]
        return auth['user_admin'] or auth['user_id'] == author

    def run(self, user_auth, param):
        result = clear_spammer(self.request, self.order)
        if result:
            return f'{self.request} 指令清除成功'
        else:
            return f'{self.request} 指令清除失敗'
