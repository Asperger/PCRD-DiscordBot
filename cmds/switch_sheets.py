from utils.log import FileLogger
from utils.google_sheets_utils import get_sheets_id
from utils.google_sheets_utils import switch_sheets as _switch_sheets

from utils.cmds_registry import register
register(cmd="switch_sheets", alias="switch_sheets")

class switch_sheets:
    def __init__(self):
        self.usage = '!switch_sheets [sheet_ID]'
        self.auth_warning = '只有公會的管理員才能使用這個功能'

    def check_param(self, param):
        return param and len(param) == 1

    def check_auth(self, auth):
        return auth['user_admin']

    def run(self, user_auth, param):
        old_id = get_sheets_id()
        (new_id, start_date, player_list) = _switch_sheets(param[0])
        if start_date and player_list:
            return f'試算表已切換為ID: {new_id}\n公會戰開始日期: {start_date.strftime("%Y/%m/%d")}'
        else:
            _switch_sheets(old_id)
            return f'試算表ID: {new_id} 錯誤或試算表格式不對'