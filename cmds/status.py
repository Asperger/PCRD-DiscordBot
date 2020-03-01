from datetime import datetime
from utils.db import query
from utils.timer import get_settlement_time
from utils.log import FileLogger
from utils.guild_member import get_guild_member_nickname, get_guild_member_list

from utils.cmds_registry import register
register(cmd="status", alias="status")

class status:
    def __init__(self):
        self.usage = '!status [YYYY-MM-DD]'
        self.auth_warning = '你不是這個公會的隊員吧?'
        self.date = get_settlement_time()

    def check_param(self, param):
        if len(param) > 1:
            return False
        elif len(param) == 1:
            try:
                datetime.strptime(param[0], '%Y-%m-%d')
            except ValueError:
                return False
            self.date = param[0]
        return True

    def check_auth(self, auth):
        user_nickname = get_guild_member_nickname(auth['guild_id'], auth['user_id'])
        if user_nickname:
            return True
        else:
            return False

    def run(self, user_auth, param):
        guild_id = user_auth['guild_id']
        user_id = user_auth['user_id']

        where = f"play_date='{self.date}' AND user_id={user_id}"
        result = query('UserTable', where)
        report = ''
        for record in result:
            user_nickname = get_guild_member_nickname(guild_id, record['user_id'])
            if not user_nickname:
                FileLogger.warn(f"Unexpected player: {record['user_id']}")
                continue

            comment = ''
            unfinished_play = 3 - (record['normal_play']+record['missing_play']+record['compensate_play'])
            if unfinished_play < 3:
                comment += f"已出{record['played_boss']}王 "
            if unfinished_play > 0:
                comment += f'仍有{unfinished_play}刀未出'

            report += f"{user_nickname} 總傷{record['damage']} 刀{record['normal_play']} 尾{record['last_play']} 補{record['compensate_play']} 閃{record['missing_play']} {comment}\n"

        if not report:
            author_nickname = get_guild_member_nickname(guild_id, user_id)
            report = f'{author_nickname}還沒出刀呢...是不是肚子餓了?'

        return report

if __name__ == '__main__':
    user_auth = {
        'guild_id': None,
        'user_id': 123,
        'user_admin': False
    }
    print(status().run(user_auth,['all']))