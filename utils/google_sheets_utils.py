import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

import pickle
import os.path
from datetime import datetime
from utils.log import FileLogger
from utils.timer import get_settlement_time_object
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

scopes = ['https://www.googleapis.com/auth/spreadsheets']
creds_path = os.path.join(os.path.dirname(__file__), 'credentials.json')
creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(creds_path, scopes)
        creds = flow.run_console()
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('sheets', 'v4', credentials=creds)

spreadsheet_id = ''
start_date = datetime.now()
player_list = {}
_undo = {}
_undo['undostack'] = []
_undo['redostack'] = []

def switch_sheets(sheet_id):
    global spreadsheet_id
    spreadsheet_id = sheet_id

def read_sheet(range_name):
    sheets = service.spreadsheets()
    result = sheets.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    return result.get('values', [])

def write_sheet(range_name, body, option='RAW'):
    sheets = service.spreadsheets()
    result = sheets.values().update(spreadsheetId=spreadsheet_id, range=range_name, body=body, valueInputOption=option).execute()
    return result

def get_start_date():
    global start_date
    values = read_sheet('角色列表!A2:A2')

    if not values:
        FileLogger.error('No player list found.')
        return
    else:
        date_tokens = values[0][0].split('/')
        settlement_time = get_settlement_time_object()
        start_date = datetime(year=int(date_tokens[0]), month=int(date_tokens[1]), day=int(date_tokens[2])).replace(tzinfo=settlement_time.tzinfo)
        return start_date

def get_player_list():
    global player_list
    values = read_sheet('角色列表!A3:B')

    if not values:
        FileLogger.error('No player list found.')
        return
    else:
        player_list = {}
        for row in values:
            player_list[int(row[1])] = int(row[0])*3
        return player_list

def fill_sheet(player_discord_id, description, boss_tag, damage, option=''):
    global _undo
    player_offset = player_list[player_discord_id]

    today = get_settlement_time_object()
    play_day_offset = today - start_date
    row_number = 3 + 6 * play_day_offset.days + (3 if option == '補' else 0)
    row_offset = 2 if option == '補' else 5

    range_name = f'輸入區!{column_number_to_letter(player_offset)}{row_number}:{column_number_to_letter(player_offset+1)}{row_number+row_offset}'
    current_state = read_sheet(range_name)
    found_cell = False
    for index in range(len(current_state)):
        if not current_state[index]:
            row_number += index
            found_cell = True
            break

    if not found_cell:
        if len(current_state) < row_offset+1:
            row_number += len(current_state)
        else:
            FileLogger.error(f'Table runs out of space: {description}')
            return False

    body = {
        'values': [
            [
                boss_tag, damage
            ]
        ]
    }

    range_name = f'輸入區!{column_number_to_letter(player_offset)}{row_number}:{column_number_to_letter(player_offset+1)}{row_number}'
    result = write_sheet(range_name, body)
    updated_range = result.get('updatedRange')
    if updated_range:
        _undo['undostack'].append([updated_range, body, description])
        _undo['redostack'] = []
        return True
    else:
        FileLogger.error(f'Fail to write sheet: {description}')
        return False

def undo():
    global _undo
    op = _undo['undostack'][-1]
    _undo['undostack'] = _undo['undostack'][0:-1]
    (range_name, body, description) = op

    empty_body = {
        'values': [
            [
                '', ''
            ]
        ]
    }
    result = write_sheet(range_name, empty_body)

    updated_range = result.get('updatedRange')
    if updated_range and range_name == updated_range:
        _undo['redostack'].append([updated_range, body, description])
        return description
    else:
        FileLogger.error(f'Inconsistent undo result: {description}')

def redo():
    global _undo
    op = _undo['redostack'][-1]
    _undo['redostack'] = _undo['redostack'][0:-1]
    (range_name, body, description) = op

    result = write_sheet(range_name, body)

    updated_range = result.get('updatedRange')
    if updated_range and range_name == updated_range:
        _undo['undostack'].append([updated_range, body, description])
        return description
    else:
        FileLogger.error(f'Inconsistent redo result: {description}')

def column_number_to_letter(input_column_number):
    output_column_name = ""
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base = len(chars)
    temp = input_column_number
    while temp > 0:
        position = temp % base
        output_column_name = ('Z' if position == 0 else chars[position - 1 if position > 0 else 0]) + output_column_name
        temp = (temp - 1) // base
    return output_column_name

if __name__ == '__main__':
    assert(column_number_to_letter(89) == 'CK')
    assert(column_number_to_letter(78) == 'BZ')
    switch_sheets('1eucoItgkCSRhV46XKqMEGmNG_5Ob6Es2O60ordUc-_4')
    print(get_start_date())
    print(get_player_list())
    fill_sheet(538023210864738314, '親愛的 fill 6-5 2856005', '6-5', 2856005)
    undo()
    redo()