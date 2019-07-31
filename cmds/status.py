import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
import utils.db
import utils.timer
from utils.log import FileLogger
from utils.guild_member import get_guild_member_nickname, get_guild_member_list

import datetime

class status:
    def __init__(self):
        self.usage = '!status [all] [YYYY-MM-DD]'
        self.date = utils.timer.get_settlement_time()
        self.all_user = False

    def check_param(self, param):
        if len(param) > 2:
            return False
        for p in param:
            if p == 'all':
                self.all_user = True
            else:
                try:
                    datetime.datetime.strptime(p, '%Y-%m-%d')
                except ValueError:
                    return False
                self.date = p
        return True

    def run(self, guild_id, user_id, *param):
        if not param or len(param[0]) == 0:
            pass
        elif not self.check_param(param[0]):
            return self.usage
        where = f"play_date='{self.date}'"
        if not self.all_user:
            where += f' AND user_id={user_id}'

        result = utils.db.query('UserTable', where)
        report = ''
        member_list = get_guild_member_list(guild_id)
        player_count = len(member_list)
        total_unfinished_play = 0
        for record in result:
            user_nickname = get_guild_member_nickname(guild_id, record['user_id'])
            if not user_nickname:
                FileLogger.warn(f"Unexpected player: {record['user_id']}")
                continue

            comment = ''
            unfinished_play = abs(3 - (record['normal_play']+record['missing_play']+record['compensate_play']))
            total_unfinished_play += unfinished_play
            if unfinished_play > 0:
                comment = f'仍有{unfinished_play}刀未出'

            report += f"{user_nickname} 總傷{record['damage']} 刀{record['normal_play']} 尾{record['last_play']} 補{record['compensate_play']} 閃{record['missing_play']} {comment}\n"
            member_list.remove(record['user_id'])

        if self.all_user:
            if player_count == len(member_list):
                report = '還沒有人出刀呢...大家是不是肚子餓了?'
            else:
                report += f'{" ".join(member_list)}未出刀'
        elif not report:
            author_nickname = get_guild_member_nickname(guild_id, user_id)
            if author_nickname:
                report = f'{author_nickname}還沒出刀呢...是不是肚子餓了?'
            else:
                report = '你不是這個公會的隊員吧?'

        return report

if __name__ == '__main__':
    print(status().run(None,123,['all']))