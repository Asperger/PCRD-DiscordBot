import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
import utils.db
from utils.log import FileLogger

import time
import utils.timer
from utils.guild_member import get_guild_member_nickname

import json

class total:
    def __init__(self):
        self.usage = '!total'

    def run(self, guild_id, user_id, *param):
        if param and len(param[0]) > 0:
            return self.usage

        elapsed_time = time.time() - utils.timer.timer_total
        if elapsed_time < 30:
            return '肚子餓了...'
        utils.timer.timer_total = time.time()

        period = utils.db.find_last_period()
        if not period or len(period) != 2:
            return

        where = f"play_date between '{period[0]}' and '{period[1]}'"
        result = utils.db.query('TimeTable', where)
        report = {}
        for record in result:
            user_nickname = get_guild_member_nickname(guild_id, record['user_id'])
            if not user_nickname:
                FileLogger.warn(f"Unexpected player: {record['user_id']}")
                continue

            stage = '3階'
            if record['rounds'] < 4:
                stage = '1階'
            elif record['rounds'] < 12:
                stage = '2階'
            boss_str = str(record['boss'])+'王'

            if user_nickname not in report:
                report[user_nickname] = {}
            if stage not in report[user_nickname]:
                report[user_nickname][stage] = {}
            if boss_str not in report[user_nickname][stage]:
                report[user_nickname][stage][boss_str] = 0

            report[user_nickname][stage][boss_str] += record['damage']

        return json.dumps(report, sort_keys=True, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    print(total().run(None,123))