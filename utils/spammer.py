from collections import deque
import os.path as path
import threading
import random
import itertools
import bisect
from utils.log import FileLogger

spam_setting_path = path.join(path.dirname(__file__), 'spam.setting')
spam_setting = {}
spam_lock = threading.Lock()
spam_limit = 5

if path.exists(spam_setting_path):
    with open(spam_setting_path, 'r', encoding="utf-8") as f:
        spam_setting_str = f.read()
        if spam_setting_str:
            try:
                spam_setting = eval(spam_setting_str)
            except Exception as e:
                FileLogger.error(f'Fail to read spam setting: {str(e)}')
                spam_setting = {}

def revert_accumulate(arr):
    reverted = [arr[0]] * len(arr)
    for i in reversed(range(1, len(arr))):
        reverted[i] = arr[i] - arr[i-1]
    return reverted

# weight initializaition
def weight_init(request):
    if request in spam_setting:
        with spam_lock:
            spam_setting[request]["weight"] = deque(itertools.accumulate([1] * len(spam_setting[request]["list"])))

def pop_spammer(request):
    if request in spam_setting:
        spam_setting[request]["weight"].pop()
        spam_setting[request]["list"].pop()

def popleft_spammer(request):
    if request in spam_setting:
        popped = spam_setting[request]["weight"][0]
        for k,v in enumerate(spam_setting[request]["weight"]):
            spam_setting[request]["weight"][k] = v - popped
        spam_setting[request]["weight"].popleft()
        spam_setting[request]["list"].popleft()

def backup():
    with spam_lock:
        with open(spam_setting_path, 'w', encoding="utf-8") as f:
            try:
                f.write(repr(spam_setting))
            except Exception as e:
                FileLogger.error(f'Fail to write spam setting: {str(e)}')

def set_spammer_weight(request, weight):
    global spam_setting
    result = False

    with spam_lock:
        if request in spam_setting:
            if len(weight) == len(spam_setting[request]["list"]):
                spam_setting[request]["weight"] = deque(itertools.accumulate(weight))
                result = True

    if result:
        backup()
    return result

def set_spammer(request, response):
    global spam_setting

    with spam_lock:
        if request in spam_setting:
            spam_setting[request]["weight"].append(spam_setting[request]["weight"][-1]+1)
            spam_setting[request]["list"].append(response)

            if len(spam_setting[request]["list"]) > spam_limit:
                popleft_spammer(request)
        else:
            spam_setting[request] = {"index": -1, "list": deque([response]), "weight":deque([1])}
            spam_setting[request]["weight"] = deque(itertools.accumulate(spam_setting[request]["weight"]))

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
                popleft_spammer(request)
            elif mode < 0:
                pop_spammer(request)
            result = True

    if result:
        backup()
    return result

def get_spammer(request):
    global spam_setting
    result = None

    if request in spam_setting:
        # no use for random pick
        #index = (spam_setting[request]["index"] + 1) % len(spam_setting[request]["list"])
        #spam_setting[request]["index"] = index
        index = bisect.bisect_left(spam_setting[request]["weight"], random.randint(1, spam_setting[request]["weight"][-1]))
        result = spam_setting[request]["list"][index]

    return result

def list_spammer(request):
    result = {}
    if request:
        if request in spam_setting:
            # weight initializaition
            if "weight" not in spam_setting[request]:
                weight_init(request)
            result[request] = revert_accumulate(spam_setting[request]["weight"])
    else:
        for key in spam_setting:
            # weight initializaition
            if "weight" not in spam_setting[key]:
                weight_init(request)
            result[key] = revert_accumulate(spam_setting[key]["weight"])
    return result

if __name__ == '__main__':
    print(list_spammer('<:REDiveCrystal:628287087237660692>'))
    set_spammer_weight('<:REDiveCrystal:628287087237660692>', [795,180,25])
    print(list_spammer('<:REDiveCrystal:628287087237660692>'))
    print(get_spammer('<:REDiveCrystal:628287087237660692>'))