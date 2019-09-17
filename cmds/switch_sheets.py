import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from utils.log import FileLogger
import utils.google_sheets_utils as sheet

class switch_sheets:
    def __init__(self):
        self.usage = '!switch_sheets [sheet_ID]'

    def check_param(self, param):
        if len(param) != 1:
            return False
        else:
            return True

    def run(self, user_auth, *param):
        if not self.check_param(param[0]):
            return self.usage
        if not user_auth['user_admin']:
            return '只有公會的管理員才能使用這個功能'

        old_id = sheet.get_sheets_id()
        sheet.switch_sheets(param[0][0])
        start_date = sheet.get_start_date()
        player_list = sheet.get_player_list()
        if start_date and player_list:
            return f'試算表已切換為ID: {param[0][0]}'
        else:
            sheet.switch_sheets(old_id)
            sheet.get_start_date()
            sheet.get_player_list()
            return f'試算表ID: {param[0][0]} 錯誤或試算表格式不對'