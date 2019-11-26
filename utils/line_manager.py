import operator
import time

guild_lines = {}
line_record = {
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

def check_guild_lines(guild_id, boss_id):
    global guild_lines
    if (guild_id not in guild_lines):
        return False
    if (boss_id not in guild_lines[guild_id]):
        return False
    return True

def set_guild_lines(guild_id, boss_id):
    global guild_lines, line_record
    if (guild_id not in guild_lines):
        guild_lines[guild_id] = line_record
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

def get_line(guild_id, boss_id):
    global guild_lines
    if not check_guild_lines(guild_id, boss_id):
        return None

    amount = guild_lines[guild_id][boss_id]["amount"]
    sorted_line = sorted(guild_lines[guild_id][boss_id]["player_ids"].items(), key=operator.itemgetter(1))
    sorted_players = list(map(lambda x: x[0], sorted_line))
    if (amount > 0):
        return sorted_players[:amount]
    else:
        return sorted_players
