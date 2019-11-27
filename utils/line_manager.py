import operator
import time

guild_lines = {}

def clear(guild_id):
    global guild_lines
    if (guild_id in guild_lines):
        del guild_lines[guild_id]
        return True
    else:
        return False

def check_guild_lines(guild_id, boss_id):
    if (guild_id not in guild_lines):
        return False
    if (boss_id not in guild_lines[guild_id]):
        return False
    return True

def set_guild_lines(guild_id, boss_id):
    global guild_lines
    if (guild_id not in guild_lines):
        guild_lines[guild_id] = {
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
    if (boss_id not in guild_lines[guild_id]):
        return False
    return True

def line_up(guild_id, user_id, boss_id):
    global guild_lines
    if not set_guild_lines(guild_id, boss_id):
        return False

    if user_id not in guild_lines[guild_id][boss_id]["player_ids"]:
        guild_lines[guild_id][boss_id]["player_ids"][user_id] = time.clock()
        return True
    else:
        return False

def line_off(guild_id, user_id, boss_id):
    global guild_lines
    if not check_guild_lines(guild_id, boss_id):
        return False

    if user_id not in guild_lines[guild_id][boss_id]["player_ids"]:
        return False
    else:
        del guild_lines[guild_id][boss_id]["player_ids"][user_id]
        return True

def set_line(guild_id, boss_id, amount):
    global guild_lines
    if not set_guild_lines(guild_id, boss_id):
        return False

    guild_lines[guild_id][boss_id]["amount"] = amount
    return True

def get_line(guild_id, boss_id, offset):
    if not check_guild_lines(guild_id, boss_id):
        return None

    amount = guild_lines[guild_id][boss_id]["amount"]
    sorted_line = sorted(guild_lines[guild_id][boss_id]["player_ids"].items(), key=operator.itemgetter(1))
    sorted_players = list(map(lambda x: x[0], sorted_line))
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
    line_up(guild_id, 100001, boss_id)
    line_up(guild_id, 100002, boss_id)
    line_up(guild_id, 100003, boss_id)
    line_up(guild_id, 100004, boss_id)
    line_up(guild_id, 100005, boss_id)
    print(get_line(guild_id, boss_id, 0))
    print(get_line(guild_id, boss_id, 1))
