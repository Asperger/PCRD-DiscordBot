from utils.log import FileLogger
from utils.spammer import set_spammer

from utils.cmds_registry import register
register(cmd="set_spam", alias="set_spam")
register(cmd="set_spam", alias="ss")

class set_spam:
    def __init__(self):
        self.usage = '!set_spam <你的指令> <佩可的反應>\n設定完成後在指令前加上驚嘆號即可使用\n指令也可以是特殊符號或表情符號\n反應也可以是特殊符號、表情符號、圖片或圖片的網址\n圖片的網址必須是直連網址，簡單來說就是以".jpg"這種檔案格式為結尾的網址\n每種指令最多可以保留5個反應'
        self.auth_warning = ''

    def check_param(self, param):
        return len(param) == 2

    def check_auth(self, auth):
        return True

    def run(self, user_auth, param):
        result = set_spammer(param[0], param[1], user_auth['user_id'])
        if result:
            return '嘿嘿'
        else:
            return '肚子餓了...'