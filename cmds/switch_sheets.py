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

    def run(self, guild_id, user_id, *param):
        if not self.check_param(param[0]):
            return self.usage
        # check authentication

        old_id = sheet.get_sheets_id()
        sheet.switch_sheets(param[0][0])
        start_date = sheet.get_start_date()
        if start_date:
            return f'試算表已切換為ID: {param[0][0]}'
        else:
            sheet.switch_sheets(old_id)
            return f'試算表ID: {param[0][0]} 錯誤或試算表格式不對'