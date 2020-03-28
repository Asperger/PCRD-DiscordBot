from os.path import exists, dirname, join
from collections import deque
from threading import Lock
from random import randint
from itertools import accumulate
from bisect import bisect_left

from utils.log import FileLogger
from utils.backup_dict import BackupDict
from utils.func_registry import register

_spam_setting_path = join(dirname(__file__), 'spam.setting')
_spam_setting = BackupDict()
_spam_setting.setpath(_spam_setting_path)
_spam_limit = 5

def backup():
    _spam_setting.backup()

register(backup)

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

def set_spammer_weight(request, weight):
    global _spam_setting
    result = False

    with _spam_setting._lock:
        if request in _spam_setting:
            if len(weight) == len(_spam_setting[request]["list"]):
                _spam_setting[request]["weight"] = deque(accumulate(weight))
                result = True

    if result:
        backup()
    return result

def set_spammer(request, response):
    global _spam_setting

    with _spam_setting._lock:
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

    with _spam_setting._lock:
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

def rename_spammer(request, name):
    if request not in _spam_setting:
        return f'目前沒有 {request} 這個指令'
    if name in _spam_setting:
        return f'目前已經有 {name} 這個指令了'

    _spam_setting[name] = _spam_setting[request]
    del _spam_setting[request]
    backup()
    return ''

if __name__ == '__main__':
    print(list_spammer(''))
    set_spammer_weight('<:REDiveCrystal:628287087237660692>', [795,180,25])
    print(list_spammer('<:REDiveCrystal:628287087237660692>'))
    print(get_spammer('<:REDiveCrystal:628287087237660692>'))