import pickle
import os.path as path
import threading
from datetime import datetime
from utils.log import FileLogger
from utils.timer import get_settlement_time_object
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

_scopes = ['https://www.googleapis.com/auth/spreadsheets']
_creds_path = path.join(path.dirname(__file__), 'credentials.json')
_pickle_path = path.join(path.dirname(__file__), 'token.pickle')
_sheet_id_path = path.join(path.dirname(__file__), 'sheet.id')
_creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if path.exists(_pickle_path):
    with open(_pickle_path, 'rb') as token:
        _creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not _creds or not _creds.valid:
    if _creds and _creds.expired and _creds.refresh_token:
        _creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(_creds_path, _scopes)
        _creds = flow.run_console()
    # Save the credentials for the next run
    with open(_pickle_path, 'wb') as token:
        pickle.dump(_creds, token)

_service = build('sheets', 'v4', credentials=_creds)

_spreadsheet_id = ''
_start_date = datetime.now()
_player_list = {}

_undo = {}
_undo['undostack'] = []
_undo['redostack'] = []
_sheet_lock = threading.RLock()

def get_sheets_id():
    global _spreadsheet_id
    return _spreadsheet_id

def read_sheet(range_name):
    try:
        sheets = _service.spreadsheets()
        result = sheets.values().get(spreadsheetId=_spreadsheet_id, range=range_name).execute()
    except Exception as e:
        FileLogger.error(f'Fail to read sheet: ID={_spreadsheet_id}, range={range_name}\n'+ str(e))
        return
    return result.get('values', [])

def write_sheet(range_name, body, option='RAW'):
    try:
        sheets = _service.spreadsheets()
        result = sheets.values().update(spreadsheetId=_spreadsheet_id, range=range_name, body=body, valueInputOption=option).execute()
    except Exception as e:
        FileLogger.error(f'Fail to write sheet: ID={_spreadsheet_id}, range={range_name}\n'+ str(e))
        return
    return result

def append_sheet(range_name, body, option='RAW'):
    try:
        sheets = _service.spreadsheets()
        result = sheets.values().append(spreadsheetId=_spreadsheet_id, range=range_name, body=body, valueInputOption=option).execute()
    except Exception as e:
        FileLogger.error(f'Fail to append sheet: ID={_spreadsheet_id}, range={range_name}\n'+ str(e))
        return
    return result

def get_start_date():
    global _start_date
    values = read_sheet('隊員列表!A1:A1')

    if not values:
        FileLogger.error('No start date found.')
        return None
    else:
        date_tokens = values[0][0].split('/')
        settlement_time = get_settlement_time_object()
        _start_date = datetime(year=int(date_tokens[0]), month=int(date_tokens[1]), day=int(date_tokens[2])).replace(tzinfo=settlement_time.tzinfo)
        return _start_date

def get_player_list():
    global _player_list
    values = read_sheet('隊員列表!B2:C')

    if not values:
        FileLogger.error('No player list found.')
        return None
    else:
        _player_list = {}
        for row in values:
            _player_list[int(row[1])] = row[0]
        return _player_list

def switch_sheets(sheet_id):
    global _spreadsheet_id
    _spreadsheet_id = sheet_id
    start_date = get_start_date()
    player_list = get_player_list()

    with open(_sheet_id_path, 'w') as f:
        f.write(_spreadsheet_id)

    return _spreadsheet_id, start_date, player_list

def fill_sheet(player_discord_id, description, play_number, boss_tag, damage, play_option, play_miss):
    global _undo, _sheet_lock
    if player_discord_id not in _player_list:
        FileLogger.warn(f'Discord ID: {player_discord_id} not found in sheet')
        return False
    player_nickname = _player_list[player_discord_id]

    today = get_settlement_time_object()
    play_tag = f"{play_number}{'B' if play_option == '補' else 'A'}"
    missing_tag = '閃' if play_miss > 0 else ''
    body = {
        'values': [
            [
                today.strftime("%Y/%m/%d %H:%M:%S"), player_nickname, play_tag, damage, boss_tag, missing_tag
            ]
        ]
    }
    play_day_offset = today - _start_date
    range_name = f'Day {play_day_offset.days + 1}-Log!A2:F'

    _sheet_lock.acquire()
    result = append_sheet(range_name, body)
    _sheet_lock.release()

    checkResult = True
    try:
        updates = result.get('updates')
        updated_range = updates.get('updatedRange')
        _undo['undostack'].append([updated_range, body, description])
        _undo['redostack'] = []
    except Exception as e:
        FileLogger.error(f'Fail to get result: {description}\n'+ str(e))
        checkResult = False

    return checkResult

def undo():
    global _undo, _sheet_lock
    op = _undo['undostack'][-1]
    _undo['undostack'] = _undo['undostack'][0:-1]
    (range_name, body, description) = op

    empty_body = {
        'values': [
            [
                '', '', '', '', '', ''
            ]
        ]
    }

    _sheet_lock.acquire()
    result = write_sheet(range_name, empty_body)
    _sheet_lock.release()

    try:
        updated_range = result.get('updatedRange')
    except Exception as e:
        FileLogger.error(f'Fail to get undo result: {description}\n'+ str(e))

    if updated_range and range_name == updated_range:
        _undo['redostack'].append([updated_range, body, description])
        return description
    else:
        FileLogger.error(f'Inconsistent undo result: {description}')
        return None

def redo():
    global _undo, _sheet_lock
    op = _undo['redostack'][-1]
    _undo['redostack'] = _undo['redostack'][0:-1]
    (range_name, body, description) = op

    _sheet_lock.acquire()
    result = write_sheet(range_name, body)
    _sheet_lock.release()

    try:
        updated_range = result.get('updatedRange')
    except Exception as e:
        FileLogger.error(f'Fail to get redo result: {description}\n'+ str(e))

    if updated_range and range_name == updated_range:
        _undo['undostack'].append([updated_range, body, description])
        return description
    else:
        FileLogger.error(f'Inconsistent redo result: {description}')
        return None

# The file sheet.id stores the id of a specific google sheet, and is
# created automatically when the switching happens.
if path.exists(_sheet_id_path):
    with open(_sheet_id_path, 'r') as f:
        switch_sheets(f.read())

if __name__ == '__main__':
    #switch_sheets('1eucoItgkCSRhV46XKqMEGmNG_5Ob6Es2O60ordUc-_4')
    switch_sheets('1f3lGlsbr-nc4k8rNwzw1QRDAoqQhrnzXmfY8LMSeNs0')
    print(get_start_date())
    print(get_player_list())
    fill_sheet(538023210864738314, '親愛的 fill 6-5 2856005 尾', 1, '6-5', 2856005, '尾', 0)
    undo()
    redo()

    t1f = threading.Thread(target=fill_sheet, args=(538023210864738314, '親愛的 fill 6-5 2345678 閃', 2, '6-5', 2345678, '', 1))
    t1u = threading.Thread(target=undo)
    t1r = threading.Thread(target=redo)

    t2f = threading.Thread(target=fill_sheet, args=(538023210864738314, '親愛的 fill 7-1 1234567', 3, '7-1', 1234567, '', 0))
    t2u = threading.Thread(target=undo)
    t2r = threading.Thread(target=redo)

    t1f.start()
    t1u.start()
    t1r.start()

    t2f.start()
    t2u.start()
    t2r.start()

    t1f.join()
    t1u.join()
    t1r.join()

    t2f.join()
    t2u.join()
    t2r.join()