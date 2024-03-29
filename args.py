from cmds import *
from utils.log import FileLogger
from utils.cmds_registry import get_cmd

def strQ2B(ustring):
    ss = []
    for s in ustring:
        rstring = ""
        for uchar in s:
            inside_code = ord(uchar)
            # Handle fullwidth space
            if inside_code == 12288:
                inside_code = 32
            # Handle other fullwidth characters
            elif (inside_code >= 65281 and inside_code <= 65374):
                inside_code -= 65248
            rstring += chr(inside_code)
        ss.append(rstring)
    return ''.join(ss)

def parse_args(user_auth, string):
    args = strQ2B(string).split()
    response = ''
    if not args:
        return response

    # Find command, otherwise consider it as spam
    cmd = get_cmd(args[0])
    if cmd:
        args = args[1:]
    else:
        cmd = "spam"

    # Create the instance
    try:
        inst = getattr(globals()[cmd], cmd)()
    except KeyError:
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