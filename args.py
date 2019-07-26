from cmds.clear import clear
from cmds.fill import fill
from cmds.status import status
from cmds.usage import usage

def parse_args(string):
    args = string.split()
    # Create the instance
    inst = globals()[args[0]]()
    # Execute the function
    return inst.run(args[1:])