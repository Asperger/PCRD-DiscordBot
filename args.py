from cmds.total import total
from cmds.fill import fill
from cmds.status import status
from cmds.undo import undo
from cmds.redo import redo

from utils.log import FileLogger
import time
import utils.timer

def usage():
    elapsed_time = time.time() - utils.timer.timer_usage
    if elapsed_time < 30:
        return '肚子餓了...'
    utils.timer.timer_usage = time.time()
    return '!fill 填表\n!status 查看出刀情況\n!total 查看傷害報告'

def parse_args(guild_id, user_id, string):
    args = string.split()
    # Create the instance
    try:
        inst = globals()[args[0]]()
    except KeyError:
        return usage()
    except Exception:
        FileLogger.exception(f'Exception at {__file__} {__name__}')
    # Execute the function
    FileLogger.info(f'{user_id} call {args[0]} with {args[1:]}')
    try:
        return inst.run(guild_id, user_id, args[1:])
    except Exception:
        FileLogger.exception(f'Exception at {__file__} {__name__}')

if __name__ == '__main__':
    print(parse_args(None, 123, 'status 2019-07-27'))