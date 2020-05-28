from time import time
from utils.log import FileLogger
from utils.timer import timer_usage

from utils.cmds_registry import register
register(cmd="usage", alias="usage")
register(cmd="usage", alias="help")

class usage:
    def __init__(self):
        self.usage = '!help'
        self.auth_warning = ''

    def check_param(self, param):
        return len(param) == 0

    def check_auth(self, auth):
        return True

    def run(self, user_auth, param):
        global timer_usage
        elapsed_time = time() - timer_usage
        if elapsed_time < 30:
            return '肚子餓了...'
        timer_usage = time()
        return """填表功能:
`!fill`或`!f` 填表
`!fill_for`或`!ff` 幫別人填表
`!status`或`!stat` 查看出刀情況
`!undo` 取消上次輸入的內容 ***不限定使用者!!! 你會把別人輸入的紀錄取消掉!!!***
`!redo` 重新輸入上次取消的內容
`!switch_sheets` 設定公會戰報表，僅限公會管理員使用
排隊功能:
`!+1` 排隊，請在公會戰討論區使用
`!-1` 取消排隊，請在公會戰討論區使用
`!+1f` 幫別人排隊，僅限公會管理員使用
`!-1f` 幫別人取消排隊，僅限公會管理員使用
`!ping` 呼叫目前在排隊的人，請在公會戰討論區使用
`!set_line` 指定各BOSS需要的人數，僅限公會管理員使用
`!clear_line` 清空所有排隊紀錄，僅限公會管理員使用
次要功能:
`!list_spam`或`!ls` 列出目前佩可的反應
`!set_spam`或`!ss` 增加佩可的反應
`!set_spam_weight`或`!ssw` 設定各個反應的權重，僅限公會管理員使用
`!rename_spam` 重新命名一個佩可的反應，僅限公會管理員使用
`!clear_spam`或`!cs` 移除佩可的反應，僅限公會管理員使用
`!help` 重看這篇說明
在各個指令之後加上 `help` 查看使用格式
這些指令只能在一部份頻道使用，使用前請注意頻道的成員名單，如果我不在名單上代表這個頻道不能使用這些指令
如果我不在線上代表我生病了 :cry:"""
