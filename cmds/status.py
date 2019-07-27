import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from utils.db import database_utils

import datetime

class status:
    def __init__(self):
        self.usage = '!status [YYYY-MM-DD]'
        self.db_utils = database_utils()

    def check_param(self, param):
        if len(param) > 1:
            return False
        try:
            datetime.datetime.strptime(param[0], '%Y-%m-%d')
        except ValueError:
            return False
        return True

    def run(self, user_id, *param):
        if not param or len(param[0]) is 0:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        elif not self.check_param(param[0]):
            return self.usage
        else:
            date = param[0][0]
        where = 'date=\'{0}\''.format(date)

        result = self.db_utils.query('UserTable', where)
        report = '隊員 總傷害 正常刀 尾刀 補償刀 閃退刀'
        for record in result:
            report += '\n<@{0}> {1} {2} {3} {4} {5}'.format(record['user_id'], record['damage'], record['normal_play'], record['last_play'], record['compensate_play'], record['missing_play'])

        return 'status: {0}'.format(report)

if __name__ == '__main__':
    print(status().run(123))