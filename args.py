from cmds.total import total
from cmds.fill import fill
from cmds.status import status

from utils.log import FileLogger
import time
import utils.timer

def usage():
    elapsed_time = time.time() - utils.timer.timer_usage
    if elapsed_time < 30:
        return '肚子餓了...'
    utils.timer.timer_usage = time.time()
    return '!fill 填表\n !status 查看出刀情況\n !total 查看傷害報告'

def parse_args(user_id, string):
    args = string.split()
    # Create the instance
    try:
        inst = globals()[args[0]]()
    except KeyError:
        return usage()
    except Exception:
        FileLogger.exception('Exception at '+__file__+' '+__name__)
    # Execute the function
    FileLogger.info('{0} call {1} with {2}'.format(user_id, args[0], args[1:]))
    return inst.run(user_id, args[1:])

if __name__ == '__main__':
    print(parse_args(123, 'status 2019-07-27'))