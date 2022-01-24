from utils.log import FileLogger
from utils.spammer import list_spammer
from utils.guild_member import get_guild_member_nickname

from utils.cmds_registry import register
register(cmd="list_spam", alias="list_spam")
register(cmd="list_spam", alias="ls")

class list_spam:
    def __init__(self):
        self.usage = '!list_spam [指令]'
        self.auth_warning = ''

    def check_param(self, param):
        return len(param) < 2

    def check_auth(self, auth):
        return True

    def run(self, user_auth, param):
        cmd = ''
        if len(param) == 1:
            cmd = param[0]

        comment = ''
        spam_list = list_spammer(cmd)
        if cmd and spam_list:
            number = len(spam_list['list'])
            comment += f'{cmd} 共{number}種反應 權重: [{" ".join(map(str, spam_list["weight"]))}]\n'
            for i in range(number):
                comment += f'編號:{i+1} 作者:{get_guild_member_nickname(spam_list["author"][i])} {spam_list["list"][i]}\n'
        else:
            for key in spam_list:
                comment += f'{key} 共{spam_list[key]}種反應\n'

        if not comment:
            comment = '目前沒有設定反應'
        return comment