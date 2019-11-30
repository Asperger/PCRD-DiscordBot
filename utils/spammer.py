from collections import deque
import os.path as path
import threading
from utils.log import FileLogger

spam_setting_path = path.join(path.dirname(__file__), 'spam.setting')
spam_setting = {}
spam_lock = threading.Lock()
spam_limit = 5

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
    with spam_lock:
        with open(spam_setting_path, 'w') as f:
            try:
                f.write(repr(spam_setting))
            except Exception as e:
                FileLogger.error(f'Fail to write spam setting: {str(e)}')

def set_spammer(request, response):
    global spam_setting

    with spam_lock:
        if request in spam_setting:
            spam_setting[request]["list"].append(response)
            if len(spam_setting[request]["list"]) > spam_limit:
                spam_setting[request]["list"].popleft()
        else:
            spam_setting[request] = {"index": -1, "list": deque([response])}

    backup()
    return True

def clear_spammer(request, mode):
    global spam_setting
    result = False

    with spam_lock:
        if request in spam_setting:
            if mode == 0 or len(spam_setting[request]["list"]) == 1:
                del spam_setting[request]
            elif mode > 0:
                spam_setting[request]["list"].popleft()
            elif mode < 0:
                spam_setting[request]["list"].pop()
            result = True

    if result:
        backup()
    return result

def get_spammer(request):
    global spam_setting
    result = None

    with spam_lock:
        if request in spam_setting:
            index = (spam_setting[request]["index"] + 1) % len(spam_setting[request]["list"])
            spam_setting[request]["index"] = index
            result = spam_setting[request]["list"][index]

    return result

def list_spammer(request):
    result = {}
    with spam_lock:
        if request:
            if request in spam_setting:
                result[request] = len(spam_setting[request]["list"])
        else:
            for key in spam_setting:
                result[key] = len(spam_setting[key]["list"])
    return result