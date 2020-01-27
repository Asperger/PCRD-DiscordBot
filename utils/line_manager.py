from operator import itemgetter
from time import clock

_guild_lines = {}

class reserved:
    def __init__(self, id, cmt):
        self.time = clock()
        self.id = id
        self.comment = cmt

    def __lt__(self, other):
        return self.time < other.time

def clear_line(guild_id, boss_id):
    global _guild_lines
    if guild_id in _guild_lines:
        if boss_id in _guild_lines[guild_id]:
            _guild_lines[guild_id][boss_id]["player_ids"] = {}
        elif boss_id == 0:
            del _guild_lines[guild_id]
        else:
            return False
    else:
        return False
    return True

def check_guild_lines(guild_id, boss_id):
    if guild_id not in _guild_lines:
        return False
    if boss_id not in _guild_lines[guild_id]:
        return False
    return True

def set_guild_lines(guild_id, boss_id):
    global _guild_lines
    if guild_id not in _guild_lines:
        _guild_lines[guild_id] = {
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
        }

    return boss_id in _guild_lines[guild_id]

def line_up(guild_id, user_id, boss_id, comment):
    global _guild_lines
    if not set_guild_lines(guild_id, boss_id):
        return ''

    if user_id not in _guild_lines[guild_id][boss_id]["player_ids"]:
        _guild_lines[guild_id][boss_id]["player_ids"][user_id] = reserved(user_id, comment)
        return '排隊成功'
    else:
        comment_updated = ''
        if _guild_lines[guild_id][boss_id]["player_ids"][user_id].comment != comment:
            _guild_lines[guild_id][boss_id]["player_ids"][user_id].comment = comment
            comment_updated = f' 備註已更新為 {comment}'
        return f'已在隊伍中{comment_updated}'

def line_off(guild_id, user_id, boss_id):
    global _guild_lines
    if not check_guild_lines(guild_id, boss_id):
        return ''

    if user_id not in _guild_lines[guild_id][boss_id]["player_ids"]:
        return '不在隊伍中'
    else:
        del _guild_lines[guild_id][boss_id]["player_ids"][user_id]
        return '取消排隊成功'

def set_line(guild_id, boss_id, amount):
    global _guild_lines
    if not set_guild_lines(guild_id, boss_id):
        return False

    _guild_lines[guild_id][boss_id]["amount"] = amount
    return True

def get_line(guild_id, boss_id, offset):
    if not check_guild_lines(guild_id, boss_id):
        return None

    amount = _guild_lines[guild_id][boss_id]["amount"]
    sorted_line = sorted(_guild_lines[guild_id][boss_id]["player_ids"].items(), key=itemgetter(1))
    sorted_players = list(map(lambda x: x[1], sorted_line))
    if amount > 0:
        if offset > 0:
            return sorted_players[amount:amount+offset]
        else:
            return sorted_players[:amount]
    else:
        return sorted_players

if __name__ == '__main__':
    guild_id, boss_id = 123, 1
    set_line(guild_id, boss_id, 3)
    line_up(guild_id, 100001, boss_id, '')
    line_up(guild_id, 100002, boss_id, '')
    line_up(guild_id, 100003, boss_id, '')
    line_up(guild_id, 100004, boss_id, '')
    line_up(guild_id, 100005, boss_id, '')
    print(get_line(guild_id, boss_id, 0))
    print(get_line(guild_id, boss_id, 1))
