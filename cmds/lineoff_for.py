import re
from cmds.lineoff import lineoff
from utils.cmds_registry import register
register(cmd="lineoff_for", alias="lineoff_for")
register(cmd="lineoff_for", alias="-1f")

class lineoff_for:
    def __init__(self):
        self.lineoff = lineoff()
        self.usage = self.lineoff.usage.replace('!-1', '!-1f @<指定對象>')
        self.auth_warning = '只有公會的管理員才能使用這個功能'
        self.playee_id = 0

    def check_param(self, param):
        if len(param) < 1:
            return False
        else:
            match = re.search(R"^<@!?(\d{18})>$", param[0])
            if match:
                self.playee_id = int(match.group(1))
            else:
                return False
            
            return self.lineoff.check_param(param[1:])

    def check_auth(self, auth):
        return auth['user_admin'] and self.lineoff.check_auth(auth)

    def run(self, user_auth, param):
        user_auth['user_id'] = self.playee_id
        return self.lineoff.run(user_auth, param[1:])