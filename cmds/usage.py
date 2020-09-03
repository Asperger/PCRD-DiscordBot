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
        global timer_usage, usage_content
        elapsed_time = time() - timer_usage
        if elapsed_time < 30:
            return '肚子餓了...'
        timer_usage = time()
        return usage_content

usage_content = {
    "title": "Afterglow 貪吃佩可",
    "description": """在各個指令之後加上 `help` 查看使用格式""",
    "填表功能 (請在刀傷登記區使用)":
"""`!fill`或`!f` 填表
`!fill_for`或`!ff` 幫別人填表
`!status`或`!stat` 查看出刀情況
`!undo` 取消上次輸入的內容
`!redo` 重新輸入上次取消的內容""",
    "排隊功能 (請在公會戰討論區使用)":
"""`!+1` 排隊
`!-1` 取消排隊
`!+1f` 幫別人排隊
`!-1f` 幫別人取消排隊
`!ping` 呼叫目前在排隊的人""",
    "次要功能":
"""`!list_spam`或`!ls` 列出目前佩可的反應
`!set_spam`或`!ss` 增加佩可的反應
`!help` 重看這篇說明"""
}
