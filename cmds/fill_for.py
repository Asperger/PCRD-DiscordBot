import re
from cmds.fill import fill
from utils.cmds_registry import register
register(cmd="fill_for", alias="fill_for")
register(cmd="fill_for", alias="ff")

class fill_for:
    def __init__(self):
        self.filler = fill()
        self.usage = self.filler.usage.replace('!fill', '!fill_for @<代刀對象>')
        self.auth_warning = self.filler.auth_warning
        self.playee_id = 0

    def check_param(self, param):
        if len(param) < 2:
            return False
        else:
            match = re.search(R"^<@!?(\d{18})>$", param[0])
            if match:
                self.playee_id = int(match.group(1))
            else:
                return False
            
            return self.filler.check_param(param[1:])

    def check_auth(self, auth):
        return self.filler.check_auth(auth)

    def run(self, user_auth, param):
        user_auth['user_id'] = self.playee_id
        return self.filler.run(user_auth, param[1:])