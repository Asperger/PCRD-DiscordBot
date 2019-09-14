from cmds.total import total
from cmds.fill import fill
from cmds.status import status
from cmds.undo import undo
from cmds.redo import redo
from cmds.ping import ping
from cmds.lineup import lineup
from cmds.switch_sheets import switch_sheets

from utils.log import FileLogger
import time
import utils.timer

cmds_registry = {
    "total": "total",
    "fill": "fill",
    "status": "status",
    "undo": "undo",
    "redo": "redo",
    "ping": "ping",
    "+1": "lineup",
    "switch_sheets": "switch_sheets"
}

def usage():
    elapsed_time = time.time() - utils.timer.timer_usage
    if elapsed_time < 30:
        return '肚子餓了...'
    utils.timer.timer_usage = time.time()
    return '`!fill` 填表\n`!status` 查看出刀情況\n`!total` 查看傷害報告\n`!undo` 取消上次輸入的內容 ***不限定使用者!!! 你會把別人輸入的紀錄取消掉!!!***\n`!redo` 重新輸入上次取消的內容\n`!help` 重看這篇說明\n在各個指令之後加上 `help` 查看使用格式\n這些指令只能在一部份頻道使用，使用前請注意頻道的成員名單，如果我不在名單上代表這個頻道不能使用這些指令\n如果我不在線上代表我生病了 :cry:'

def parse_args(user_auth, string):
    args = string.split()
    # Create the instance
    try:
        inst = globals()[cmds_registry[args[0]]]()
    except KeyError:
        return usage()
    except IndexError:
        return usage()
    except Exception:
        FileLogger.exception(f'Exception at {__file__} {__name__}')
        return
    # Execute the function
    FileLogger.info(f"{user_auth['user_id']} call {args[0]} with {args[1:]}")
    try:
        return inst.run(user_auth, args[1:])
    except Exception:
        FileLogger.exception(f'Exception at {__file__} {__name__}')

if __name__ == '__main__':
    user_auth = {
        'guild_id': None,
        'user_id': 123,
        'user_admin': False
    }
    print(parse_args(user_auth, 'status 2019-07-27'))
