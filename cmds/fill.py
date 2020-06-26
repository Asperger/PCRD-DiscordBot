from utils.db import query, insert, upsert, sqlur
from utils.log import FileLogger
from utils.line_manager import line_off
from utils.timer import get_settlement_time
from utils.guild_member import get_guild_member_nickname
from utils.google_sheets_utils import fill_sheet

from utils.cmds_registry import register
register(cmd="fill", alias="fill")
register(cmd="fill", alias="f")

class fill:
    def __init__(self):
        self.usage = '!fill <幾周目>-<幾王> <傷害> [尾|補] [閃]\n如果你擊殺了BOSS，請加上`尾`\n如果你使用了補償時間，請加上`補`\n如果你使用了閃退，請加上`閃`'
        self.auth_warning = '你不是這個公會的隊員吧?'

    def play_type(self, x:str) -> str:
        return {
            '尾': 'last_play',
            '補': 'compensate_play'
        }.get(x, 'normal_play')  

    def check_param(self, param):
        if len(param) < 2 or len(param) > 4:
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

        if len(param) == 4:
            if param[2] not in ('尾', '補'):
                return False
            if param[3] != '閃':
                return False

        return True

    def check_auth(self, auth):
        user_nickname = get_guild_member_nickname(auth['user_id'])
        if user_nickname:
            return True
        else:
            return False

    def get_played_number(self, user_id:int, play_type:str) -> (int, int):
        date = get_settlement_time()
        where = f"play_date='{date}' AND user_id={user_id}"
        result = query('UserTable', where)
        if result:
            if play_type == 'normal_play':
                return int(result[0]['played_boss']), result[0]['normal_play'] + max(result[0]['last_play'], result[0]['compensate_play']) + 1
            else:
                return int(result[0]['played_boss']), result[0]['normal_play'] + result[0][play_type] + 1
        else:
            return 0, 1

    def run(self, user_auth, param):
        user_id = user_auth['user_id']

        user_nickname = get_guild_member_nickname(user_id)

        boss_tag = param[0]
        boss_tags = boss_tag.split('-')

        if len(param) == 3:
            ploption = param[2]
            plmiss = 1 if ploption == '閃' else 0
            pltype = self.play_type(ploption)
        elif len(param) == 4:
            ploption = param[2]
            plmiss = 1 if param[3] == '閃' else 0
            pltype = self.play_type(ploption)
        else:
            ploption = ''
            plmiss = 0
            pltype = 'normal_play'

        damage = int(param[1])
        description = f'{user_nickname} fill {" ".join(param)}'

        lastboss, plnumber = self.get_played_number(user_id, pltype)
        sheet_result = fill_sheet(user_id, description, plnumber, boss_tag, damage, ploption, plmiss)
        if not sheet_result:
            return f'{user_nickname} 試算表記錄失敗'

        column_value = {'user_id':user_id, 'rounds':int(boss_tags[0]), 'boss':int(boss_tags[1]), 'damage':int(damage), 'play_type':pltype}
        result = insert('TimeTable', column_value)
        if not result:
            return f'{user_nickname} 記錄失敗'

        column_value = {'user_id':user_id, pltype:1, 'missing_play':plmiss}
        if pltype == 'last_play':
            column_value['played_boss'] = boss_tags[1]
        db_result = upsert('UserTable', column_value, f'user_id={user_id}')
        if not db_result:
            return f'{user_nickname} 記錄失敗'

        sqlur.barrier(description)
        if pltype == 'compensate_play':
            line_off(user_id, lastboss)
        elif pltype == 'normal_play':
            line_off(user_id, int(boss_tags[1]))
        return f'{user_nickname} 記錄成功'

if __name__ == '__main__':
    user_auth = {
        'guild_id': None,
        'user_id': 123,
        'user_admin': False
    }
    print(fill().run(user_auth,['18-4','1','尾']))
    print(fill().run(user_auth,['19-5','2','尾']))
    print(fill().run(user_auth,['18-1','3']))
    print(fill().run(user_auth,['19-5','4','補']))
    print(fill().run(user_auth,['19-4','5','補']))