from cmds.total import total
from cmds.fill import fill
from cmds.status import status
from cmds.usage import usage

def parse_args(user_id, string):
    args = string.split()
    # Create the instance
    try:
        inst = globals()[args[0]]()
    except KeyError:
        inst = usage()
    # Execute the function
    return inst.run(user_id, args[1:])

if __name__ == '__main__':
    print(parse_args(123, 'status 2019-07-27'))