from os.path import exists, dirname, join
from collections import deque
from threading import Lock
from random import randint
from itertools import accumulate
from bisect import bisect_left
from utils.log import FileLogger

_spam_setting_path = join(dirname(__file__), 'spam.setting')
_spam_setting = {}
_spam_lock = Lock()
_spam_limit = 5

if exists(_spam_setting_path):
    with open(_spam_setting_path, 'r', encoding="utf-8") as f:
        spam_setting_str = f.read()
        if spam_setting_str:
            try:
                _spam_setting = eval(spam_setting_str)
            except Exception as e:
                FileLogger.error(f'Fail to read spam setting: {str(e)}')
                _spam_setting = {}

def revert_accumulate(arr):
    reverted = [arr[0]] * len(arr)
    for i in reversed(range(1, len(arr))):
        reverted[i] = arr[i] - arr[i-1]
    return reverted

def pop_spammer(request):
    if request in _spam_setting:
        _spam_setting[request]["weight"].pop()
        _spam_setting[request]["list"].pop()

def popleft_spammer(request):
    if request in _spam_setting:
        popped = _spam_setting[request]["weight"][0]
        for k,v in enumerate(_spam_setting[request]["weight"]):
            _spam_setting[request]["weight"][k] = v - popped
        _spam_setting[request]["weight"].popleft()
        _spam_setting[request]["list"].popleft()

def backup():
    with _spam_lock:
        with open(_spam_setting_path, 'w', encoding="utf-8") as f:
            try:
                f.write(repr(_spam_setting))
            except Exception as e:
                FileLogger.error(f'Fail to write spam setting: {str(e)}')

def set_spammer_weight(request, weight):
    global _spam_setting
    result = False

    with _spam_lock:
        if request in _spam_setting:
            if len(weight) == len(_spam_setting[request]["list"]):
                _spam_setting[request]["weight"] = deque(accumulate(weight))
                result = True

    if result:
        backup()
    return result

def set_spammer(request, response):
    global _spam_setting

    with _spam_lock:
        if request in _spam_setting:
            _spam_setting[request]["weight"].append(_spam_setting[request]["weight"][-1]+1)
            _spam_setting[request]["list"].append(response)

            if len(_spam_setting[request]["list"]) > _spam_limit:
                popleft_spammer(request)
        else:
            _spam_setting[request] = {"index": -1, "list": deque([response]), "weight":deque([1])}
            _spam_setting[request]["weight"] = deque(accumulate(_spam_setting[request]["weight"]))

    backup()
    return True

def clear_spammer(request, mode):
    global _spam_setting
    result = False

    with _spam_lock:
        if request in _spam_setting:
            if mode == 0 or len(_spam_setting[request]["list"]) == 1:
                del _spam_setting[request]
            elif mode > 0:
                popleft_spammer(request)
            elif mode < 0:
                pop_spammer(request)
            result = True

    if result:
        backup()
    return result

def get_spammer(request):
    global _spam_setting
    result = None

    if request in _spam_setting:
        # no use for random pick
        #index = (spam_setting[request]["index"] + 1) % len(spam_setting[request]["list"])
        #spam_setting[request]["index"] = index
        index = bisect_left(_spam_setting[request]["weight"], randint(1, _spam_setting[request]["weight"][-1]))
        result = _spam_setting[request]["list"][index]

    return result

def list_spammer(request):
    result = {}
    if request:
        if request in _spam_setting:
            result["weight"] = revert_accumulate(_spam_setting[request]["weight"])
            result["list"] = _spam_setting[request]["list"]
    else:
        for key in _spam_setting:
            result[key] = len(_spam_setting[key]["list"])
    return result

if __name__ == '__main__':
    print(list_spammer(''))
    set_spammer_weight('<:REDiveCrystal:628287087237660692>', [795,180,25])
    print(list_spammer('<:REDiveCrystal:628287087237660692>'))
    print(get_spammer('<:REDiveCrystal:628287087237660692>'))