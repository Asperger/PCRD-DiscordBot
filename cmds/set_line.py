from utils.log import FileLogger
import utils.line_manager as line_manager

from utils.cmds_registry import register
register(cmd="set_line", alias="set_line")

class set_line:
    def __init__(self):
        self.usage = '!set_line <幾王> <人數>\n設定正選的人數，人數為0代表不限人數'
        self.auth_warning = '只有公會的管理員才能使用這個功能'

    def check_param(self, param):
        return len(param) == 2 and param[0].isdigit() and param[1].isdigit()

    def check_auth(self, auth):
        return auth['user_admin']

    def run(self, user_auth, param):
        comment = '設定失敗'
        boss_id = int(param[0])
        amount = int(param[1])
        result = line_manager.set_line(user_auth['guild_id'], boss_id, amount)
        if result:
            if amount < 1:
                comment = f'已設定 {boss_id}王: 不限人數'
            else:
                comment = f'已設定 {boss_id}王: {amount}人'
        return comment