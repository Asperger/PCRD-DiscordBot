import utils.db
from utils.log import FileLogger
from utils.line_manager import line_off
from utils.timer import get_settlement_time
from utils.guild_member import get_guild_member_nickname
from utils.google_sheets_utils import fill_sheet

class fill:
    def __init__(self):
        self.usage = '!fill <幾周目>-<幾王> <傷害> [尾|補] [閃]\n如果你擊殺了BOSS，請加上`尾`\n如果你使用了補償時間，請加上`補`\n如果你使用了閃退，請加上`閃`'
        self.auth_warning = '你不是這個公會的隊員吧?'

    def play_type(self, x):
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
        user_nickname = get_guild_member_nickname(auth['guild_id'], auth['user_id'])
        if user_nickname:
            return True
        else:
            return False

    def get_played_number(self, user_id):
        date = get_settlement_time()
        where = f"play_date='{date}' AND user_id={user_id}"
        result = utils.db.query('UserTable', where)
        if result:
            return result[0]['normal_play'] + result[0]['compensate_play']
        else:
            return 0

    def run(self, user_auth, param):
        guild_id = user_auth['guild_id']
        user_id = user_auth['user_id']

        user_nickname = get_guild_member_nickname(guild_id, user_id)

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

        plnumber = self.get_played_number(user_id) + 1
        sheet_result = fill_sheet(user_id, description, plnumber, boss_tag, damage, ploption, plmiss)
        if not sheet_result:
            return f'{user_nickname} 試算表記錄失敗'

        column_value = {'user_id':user_id, 'rounds':boss_tags[0], 'boss':boss_tags[1], 'damage':damage}
        result = utils.db.insert('TimeTable', column_value)
        if not result:
            return f'{user_nickname} 記錄失敗'

        column_value = {'user_id':user_id, 'damage':damage, pltype:1, 'played_boss':str(boss_tags[1]), 'missing_play':plmiss}
        db_result = utils.db.upsert('UserTable', column_value, f'user_id={user_id}')
        if not db_result:
            return f'{user_nickname} 記錄失敗'

        utils.db.sqlur.barrier(description)
        line_off(guild_id, user_id, int(boss_tags[1]))
        return f'{user_nickname} 記錄成功'

if __name__ == '__main__':
    user_auth = {
        'guild_id': None,
        'user_id': 123,
        'user_admin': False
    }
    print(fill().run(user_auth,['18-4','1722996','尾']))