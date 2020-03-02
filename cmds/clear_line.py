from utils.log import FileLogger
from utils.line_manager import clear_line as _clear_line

from utils.cmds_registry import register
register(cmd="clear_line", alias="clear_line")

class clear_line:
    def __init__(self):
        self.usage = '!clear_line [幾王]\n不指定王將清除所有排隊紀錄'
        self.auth_warning = '只有公會的管理員才能使用這個功能'
        self.boss = 0

    def check_param(self, param):
        result = True
        if not param:
            pass
        elif len(param) == 1 and param[0].isdigit():
            b = int(param[0])
            if b > 0 and b < 6:
                self.boss = b
            else:
                result = False
        else:
            result = False
        return result

    def check_auth(self, auth):
        return auth['user_admin']

    def run(self, user_auth, *param):
        comment = '設定失敗'
        result = _clear_line(self.boss)
        if result:
            if self.boss == 0:
                comment = '排隊記錄清除成功'
            else:
                comment = f'{self.boss}王 排隊記錄清除成功'
        return comment