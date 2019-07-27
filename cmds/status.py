import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
import utils.db

import datetime

class status:
    def __init__(self):
        self.usage = '!status [YYYY-MM-DD]'

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

        result = utils.db.query('UserTable', where)
        report = ''
        for record in result:
            report += '<@{0}> 總傷{1} 刀{2} 尾{3} 補{4} 閃{5}\n'.format(record['user_id'], record['damage'], record['normal_play'], record['last_play'], record['compensate_play'], record['missing_play'])

        return report

if __name__ == '__main__':
    print(status().run(123))