from os.path import exists, dirname, join
from threading import Lock
from random import randint
from itertools import accumulate
from bisect import bisect_left

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

def del_spammer(request, index):
    if request in _spam_setting:
        popped = _spam_setting[request]["weight"][index]
        for k,v in enumerate(_spam_setting[request]["weight"]):
            if k >= index:
                _spam_setting[request]["weight"][k] = v - popped
        del _spam_setting[request]["weight"][index]
        del _spam_setting[request]["list"][index]
        del _spam_setting[request]["author"][index]

def set_spammer_weight(request, weight):
    global _spam_setting
    result = False

    with _spam_setting._lock:
        if request in _spam_setting:
            if len(weight) == len(_spam_setting[request]["list"]):
                _spam_setting[request]["weight"] = accumulate(weight)
                result = True

    if result:
        backup()
    return result

def set_spammer(request, response, author):
    global _spam_setting

    with _spam_setting._lock:
        if request in _spam_setting:
            _spam_setting[request]["weight"].append(_spam_setting[request]["weight"][-1]+1)
            _spam_setting[request]["list"].append(response)
            _spam_setting[request]["author"].append(author)

            if len(_spam_setting[request]["list"]) > _spam_limit:
                del_spammer(request, 0)
        else:
            _spam_setting[request] = {"index": -1, "author": [author], "list": [response], "weight":[1]}

    backup()
    return True

def clear_spammer(request, order):
    global _spam_setting
    result = False
    number = len(_spam_setting[request]["list"])

    with _spam_setting._lock:
        if request in _spam_setting:
            if order <= 0 or order > number or number == 1:
                del _spam_setting[request]
            else:
                del_spammer(request, order - 1)
            result = True

    if result:
        backup()
    return result

def get_spammer(request, order=0):
    global _spam_setting
    result = None
    author = None

    if request in _spam_setting:
        # no use for random pick
        #index = (spam_setting[request]["index"] + 1) % len(spam_setting[request]["list"])
        #spam_setting[request]["index"] = index
        if order > 0 and order <= len(_spam_setting[request]["list"]):
            index = order - 1
        else:
            index = bisect_left(_spam_setting[request]["weight"], randint(1, _spam_setting[request]["weight"][-1]))
        result = _spam_setting[request]["list"][index]
        author = _spam_setting[request]["author"][index]

    return result, author

def list_spammer(request):
    result = {}
    if request:
        if request in _spam_setting:
            result["author"] = _spam_setting[request]["author"]
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