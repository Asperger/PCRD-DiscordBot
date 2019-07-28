import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
import utils.db

import time
import utils.timer

import json

class total:
    def __init__(self):
        self.usage = '!total'

    def run(self, user_id, *param):
        if param and len(param[0]) > 0:
            return self.usage

        elapsed_time = time.time() - utils.timer.timer_total
        if elapsed_time < 30:
            return '肚子餓了...'
        utils.timer.timer_total = time.time()

        period = utils.db.find_last_period()
        if not period or len(period) is not 2:
            return

        where = 'play_date between \'{0}\' and \'{1}\''.format(period[0], period[1])
        result = utils.db.query('TimeTable', where)
        report = {}
        for record in result:
            stage = '3階'
            if record['rounds'] < 4:
                stage = '1階'
            elif record['rounds'] < 12:
                stage = '2階'
            mentioned_id = '<@{0}>'.format(record['user_id'])
            boss_str = str(record['boss'])+'王'

            if mentioned_id not in report:
                report[mentioned_id] = {}
            if stage not in report[mentioned_id]:
                report[mentioned_id][stage] = {}
            if boss_str not in report[mentioned_id][stage]:
                report[mentioned_id][stage][boss_str] = 0

            report[mentioned_id][stage][boss_str] += record['damage']

        return json.dumps(report, sort_keys=True, indent=4, ensure_ascii=False).replace('{','').replace('}','').replace('\"','')

if __name__ == '__main__':
    print(total().run(123))