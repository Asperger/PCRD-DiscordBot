from utils.log import FileLogger
import utils.google_sheets_utils as sheet

class switch_sheets:
    def __init__(self):
        self.usage = '!switch_sheets [sheet_ID]'
        self.auth_warning = '只有公會的管理員才能使用這個功能'

    def check_param(self, param):
        return param and len(param) == 1

    def check_auth(self, auth):
        return auth['user_admin']

    def run(self, user_auth, param):
        old_id = sheet.get_sheets_id()
        (new_id, start_date, player_list) = sheet.switch_sheets(param[0])
        if start_date and player_list:
            return f'試算表已切換為ID: {new_id}\n公會戰開始日期: {start_date.strftime("%Y/%m/%d")}'
        else:
            sheet.switch_sheets(old_id)
            return f'試算表ID: {new_id} 錯誤或試算表格式不對'