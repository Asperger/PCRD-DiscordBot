import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
import utils.db
from utils.log import FileLogger
from utils.guild_member import get_guild_member_nickname

class fill:
    def __init__(self):
        self.usage = '!fill <幾周目>-<幾王> <傷害> [尾|補|閃]'

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
        if len(boss_tag) != 2:
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
            if param[2] == '閃' and param[1] != 0:
                return False

        return True

    def run(self, guild_id, user_id, *param):
        user_nickname = get_guild_member_nickname(guild_id, user_id)
        if not user_nickname:
            return '你不是這個公會的隊員吧?'

        if not param or len(param[0]) == 0:
            return self.usage
        if param[0][0] == 'help':
            return self.usage
        if not self.check_param(param[0]):
            return self.usage

        boss_tag = param[0][0].split('-')

        if len(param[0]) == 3:
            pltype = self.play_type(param[0][2])
        else:
            pltype = 'normal_play'


        column_value = {'user_id':user_id, 'rounds':boss_tag[0], 'boss':boss_tag[1], 'damage':param[0][1]}
        result = utils.db.insert('TimeTable', column_value)
        if not result:
            return f'{user_nickname} 記錄失敗'

        column_value = {'user_id':user_id, 'damage':param[0][1], pltype:1}
        result = utils.db.upsert('UserTable', column_value, f'user_id={user_id}')
        if result:
            utils.db.sqlur.barrier(f'{user_nickname} fill {" ".join(param[0])}')
            return f'{user_nickname} 記錄成功'
        else:
            return f'{user_nickname} 記錄失敗'

if __name__ == '__main__':
    print(fill().run(None,123,['18-4','1722996','尾']))