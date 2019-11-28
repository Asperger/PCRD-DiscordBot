from cmds.usage import usage
from cmds.fill import fill
from cmds.status import status
from cmds.undo import undo
from cmds.redo import redo
from cmds.ping import ping
from cmds.lineup import lineup
from cmds.lineoff import lineoff
from cmds.spam import spam
from cmds.set_spam import set_spam
from cmds.clear_spam import clear_spam
from cmds.set_line import set_line
from cmds.clear_line import clear_line
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
    "spam": "spam",
    "set_spam": "set_spam",
    "clear_spam": "clear_spam",
    "set_line": "set_line",
    "clear_line": "clear_line",
    "switch_sheets": "switch_sheets"
}

def parse_args(user_auth, string):
    args = string.split()
    response = ''

    # Find command, otherwise consider it as spam
    cmd = "spam"
    if args[0] in cmds_registry:
        cmd = cmds_registry[args[0]]
        args = args[1:]

    # Create the instance
    try:
        inst = globals()[cmd]()
    except KeyError:
        FileLogger.warn(f'No command found')
    except IndexError:
        FileLogger.warn(f'No command found')
    except Exception:
        FileLogger.exception(f'Exception at {__file__} {__name__}')
    
    # Execute the function
    FileLogger.info(f"{user_auth['user_id']} call {cmd} with {args}")
    try:
        if len(args) == 1 and args[0] == 'help':
            response = inst.usage
        elif not inst.check_param(args):
            response = inst.usage
        elif not inst.check_auth(user_auth):
            response = inst.auth_warning
        else:
            response = inst.run(user_auth, args)
    except Exception:
        FileLogger.exception(f'Exception at {__file__} {__name__}')

    return response

if __name__ == '__main__':
    user_auth = {
        'guild_id': None,
        'user_id': 123,
        'user_admin': False
    }
    print(parse_args(user_auth, "help"))
    print(parse_args(user_auth, 'status 2019-07-27'))
