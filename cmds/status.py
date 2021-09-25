from datetime import datetime
from utils.db import query
from utils.timer import get_settlement_time
from utils.log import FileLogger
from utils.guild_member import check_guild_crew, get_guild_member_nickname

from utils.cmds_registry import register
register(cmd="status", alias="status")
register(cmd="status", alias="stat")

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
        return check_guild_crew(auth['user_id'])

    def play_type(self, x:str) -> str:
        return {
            'last_play': '尾刀',
            'compensate_play': '補償'
        }.get(x, '')  

    def run(self, user_auth, param):
        user_id = user_auth['user_id']
        author_nickname = get_guild_member_nickname(user_id)

        where = f"play_date='{self.date}' AND user_id={user_id}"
        result = query('UserTable', where)
        report = {}
        if result:
            report["title"] = f"{self.date}出刀狀況"
            report["description"] = "已用閃退" if int(result[0]['missing_play']) > 0 else "未用閃退"

            details = query('TimeTable', where)
            for record in details:
                boss_info = f"{record['rounds']}周目{record['boss']}王"
                play_info = f"{self.play_type(record['play_type'])}{record['damage']}"
                if boss_info in report:
                    report[boss_info] += f"\n{play_info}"
                else:
                    report[boss_info] = play_info
        else:
            report = f'{author_nickname}還沒出刀呢...是不是肚子餓了?'

        return report

if __name__ == '__main__':
    user_auth = {
        'user_id': 123,
        'user_admin': False
    }
    print(status().run(user_auth,['all']))