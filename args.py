from cmds.usage import usage
from cmds.fill import fill
from cmds.status import status
from cmds.undo import undo
from cmds.redo import redo
from cmds.ping import ping
from cmds.lineup import lineup
from cmds.lineoff import lineoff
from cmds.set_line import set_line
from cmds.switch_sheets import switch_sheets

from utils.log import FileLogger
import time
import utils.timer

cmds_registry = {
    "help": "usage",
    "usage": "usage",
    "fill": "fill",
    "status": "status",
    "undo": "undo",
    "redo": "redo",
    "ping": "ping",
    "+1": "lineup",
    "lineup": "lineup",
    "-1": "lineoff",
    "lineoff": "lineoff",
    "set_line": "set_line",
    "switch_sheets": "switch_sheets"
}

def parse_args(user_auth, string):
    args = string.split()
    # Create the instance
    try:
        inst = globals()[cmds_registry[args[0]]]()
    except KeyError:
        FileLogger.warn(f'No command found')
        return
    except IndexError:
        FileLogger.warn(f'No command found')
        return
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
    print(parse_args(user_auth, "help"))
    print(parse_args(user_auth, 'status 2019-07-27'))
