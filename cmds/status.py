import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
import utils.db
from utils.log import FileLogger

import datetime

class status:
    def __init__(self):
        self.usage = '!status [all] [YYYY-MM-DD]'
        self.date = datetime.datetime.now().strftime("%Y-%m-%d")
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

    def run(self, client, user_id, *param):
        if not param or len(param[0]) == 0:
            pass
        elif not self.check_param(param[0]):
            return self.usage
        where = 'play_date=\'{0}\''.format(self.date)
        if not self.all_user:
            where += ' AND user_id={0}'.format(user_id)

        result = utils.db.query('UserTable', where)
        report = ''
        player_count = 0
        total_unfinished_play = 0
        for record in result:
            user = client.get_user(record['user_id'])
            if not user:
                FileLogger.warn('Unexpected player: {0}'.format(user_id))
                continue
            comment = ''
            player_count += 1
            unfinished_play = 3 - (record['normal_play']+record['missing_play']+record['compensate_play'])
            total_unfinished_play += unfinished_play
            if unfinished_play > 0:
                comment = '仍有{0}刀未出'.format(unfinished_play)
            report += '{0} 總傷{1} 刀{2} 尾{3} 補{4} 閃{5} {6}\n'.format(user.display_name, record['damage'], record['normal_play'], record['last_play'], record['compensate_play'], record['missing_play'], comment)

        if self.all_user:
            report += '共{0}刀未出'.format((30-player_count)*3+total_unfinished_play)

        return report

if __name__ == '__main__':
    print(status().run(None,123,['all']))