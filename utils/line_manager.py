from operator import itemgetter
from os.path import dirname, join

from utils.log import FileLogger
from utils.backup_dict import BackupDict
from utils.reserved import reserved
from utils.func_registry import register

_guild_lines = BackupDict({
            1: {
                "amount": 0,
                "player_ids": {}
            },
            2: {
                "amount": 0,
                "player_ids": {}
            },
            3: {
                "amount": 0,
                "player_ids": {}
            },
            4: {
                "amount": 0,
                "player_ids": {}
            },
            5: {
                "amount": 0,
                "player_ids": {}
            },
        })
_guild_lines_path = join(dirname(__file__), 'guild.lines')
_guild_lines.setpath(_guild_lines_path)

_time_offset = 0
for boss in _guild_lines.values():
    for player in boss["player_ids"].values():
        _time_offset = max(_time_offset, player.time)

def backup():
    _guild_lines.backup()

register(backup)

def clear_line(boss_id:int) -> bool:
    global _guild_lines
    if boss_id in _guild_lines:
        _guild_lines[boss_id]["player_ids"] = {}
    elif boss_id == 0:
        for key in _guild_lines:
            _guild_lines[key]["player_ids"] = {}
    else:
        return False
    backup()
    FileLogger.info('clear_line executed')
    return True

def check_guild_lines(boss_id:int) -> bool:
    return boss_id in _guild_lines

def line_up(user_id:int, boss_id:int, comment:str) -> str:
    global _guild_lines
    if not check_guild_lines(boss_id):
        return ''

    if user_id not in _guild_lines[boss_id]["player_ids"]:
        _guild_lines[boss_id]["player_ids"][user_id] = reserved(user_id, comment, _time_offset)
        return '排隊成功'
    else:
        comment_updated = ''
        if _guild_lines[boss_id]["player_ids"][user_id].comment != comment:
            _guild_lines[boss_id]["player_ids"][user_id].comment = comment
            comment_updated = f' 備註已更新為 {comment}'
        return f'已在隊伍中{comment_updated}'

def line_off(user_id:int, boss_id:int) -> str:
    global _guild_lines
    if not check_guild_lines(boss_id):
        return ''

    if user_id not in _guild_lines[boss_id]["player_ids"]:
        return '不在隊伍中'
    else:
        del _guild_lines[boss_id]["player_ids"][user_id]
        return '取消排隊成功'

def set_line(boss_id:int, amount:int) -> bool:
    global _guild_lines
    if not check_guild_lines(boss_id):
        return False

    _guild_lines[boss_id]["amount"] = amount
    return True

def get_line(boss_id:int, offset:int, list_all:bool) -> list:
    if not check_guild_lines(boss_id):
        return None

    amount = _guild_lines[boss_id]["amount"]
    sorted_line = sorted(_guild_lines[boss_id]["player_ids"].items(), key=itemgetter(1))
    sorted_players = list(map(lambda x: x[1], sorted_line))
    if amount > 0 and not list_all:
        if offset > 0:
            return sorted_players[amount:amount+offset]
        else:
            return sorted_players[:amount]
    else:
        return sorted_players

if __name__ == '__main__':
    boss_id = 1
    set_line(boss_id, 3)
    line_up(100001, boss_id, '')
    line_up(100002, boss_id, '')
    line_up(100003, boss_id, '')
    line_up(100004, boss_id, '')
    line_up(100005, boss_id, '')
    line_up(100006, boss_id, '')
    line_up(100007, boss_id, '')
    print(*get_line(boss_id, 0, True), sep='\n')
    print(*get_line(boss_id, 1, False), sep='\n')
    line_off(100003, boss_id)
    print(*get_line(boss_id, 0, False), sep='\n')
    print(*get_line(boss_id, 1, False), sep='\n')
    print(*get_line(boss_id, 2, False), sep='\n')
