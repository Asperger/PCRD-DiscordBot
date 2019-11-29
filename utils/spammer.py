from collections import deque
import os.path as path
from utils.log import FileLogger

spam_setting_path = path.join(path.dirname(__file__), 'spam.setting')
spam_setting = {}
if path.exists(spam_setting_path):
    with open(spam_setting_path, 'r') as f:
        spam_setting_str = f.read()
        if spam_setting_str:
            try:
                spam_setting = eval(spam_setting_str)
            except Exception as e:
                FileLogger.error(f'Fail to read spam setting: {str(e)}')
                spam_setting = {}

def backup():
    with open(spam_setting_path, 'w') as f:
        try:
            f.write(repr(spam_setting))
        except Exception as e:
            FileLogger.error(f'Fail to write spam setting: {str(e)}')

def set_spammer(request, response):
    global spam_setting
    if request in spam_setting:
        spam_setting[request]["list"].append(response)
    else:
        spam_setting[request] = {"index": -1, "list": deque([response])}

    backup()
    return True

def clear_spammer(request, mode):
    global spam_setting
    if request in spam_setting:
        if mode == 0 or len(spam_setting[request]["list"]) == 1:
            del spam_setting[request]
        elif mode > 0:
            spam_setting[request]["list"].popleft()
        elif mode < 0:
            spam_setting[request]["list"].pop()

        backup()
        return True
    else:
        return False

def get_spammer(request):
    global spam_setting
    result = None
    if request in spam_setting:
        index = (spam_setting[request]["index"] + 1) % len(spam_setting[request]["list"])
        spam_setting[request]["index"] = index
        result = spam_setting[request]["list"][index]
    return result
