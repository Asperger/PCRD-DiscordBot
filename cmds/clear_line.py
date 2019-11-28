import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from utils.log import FileLogger
import utils.line_manager as line_manager

class clear_line:
    def __init__(self):
        self.usage = '!clear_line'
        self.auth_warning = '你不是這個公會的隊員吧?'

    def check_param(self, param):
        return not param

    def check_auth(self, auth):
        return auth['user_admin']

    def run(self, user_auth, *param):
        result = line_manager.clear(user_auth['guild_id'])
        if result:
            return '排隊記錄清除成功'
        else:
            return '目前沒有排隊記錄'