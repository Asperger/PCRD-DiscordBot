import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from utils.db import database_utils

class fill:
    def __init__(self):
        self.usage = '!fill <幾周目>-<幾王> <傷害> [尾|補|閃]'
        self.db_utils = database_utils()

    def play_type(self, x):
        return {
            '尾': 'last_play',
            '補': 'compensate_play',
            '閃': 'missing_play'
        }.get(x, 'normal_play')  

    def check_param(self, param):
        if len(param) < 2 or len(param) > 3:
            return False

        boss_tag = param[0].split('-')
        if len(boss_tag) is not 2:
            return False
        if not boss_tag[0].isdigit():
            return False
        if not boss_tag[1].isdigit():
            return False

        if not param[1].isdigit():
            return False

        if len(param) == 3:
            if param[2] not in ('尾', '補', '閃'):
                return False

        return True

    def run(self, user_id, *param):
        if not param or len(param[0]) is 0:
            return self.usage
        if param[0][0] is 'help':
            return self.usage
        if not self.check_param(param[0]):
            return self.usage

        boss_tag = param[0][0].split('-')
        column_value = {'user_id':user_id, 'rounds':boss_tag[0], 'boss':boss_tag[1], 'damage':param[0][1]}
        result = self.db_utils.insert('TimeTable', column_value)

        if len(param) is 3:
            pltype = self.play_type(param[2])
        else:
            pltype = 'normal_play'
        column_value = {'user_id':user_id, 'damage':param[0][1], pltype:1}
        result = self.db_utils.upsert('UserTable', column_value, 'user_id={0}'.format(user_id), True)
        return 'fill: {0}'.format(result)

if __name__ == '__main__':
    print(fill().run(123))