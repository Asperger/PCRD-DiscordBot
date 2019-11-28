spam_setting = {}

def set_spammer(request, response):
    global spam_setting
    if request in spam_setting:
        spam_setting[request]["list"].append(response)
    else:
        spam_setting[request] = {"index": 0, "list": [response]}
    return True

def clear_spammer(request):
    global spam_setting
    if request in spam_setting:
        del spam_setting[request]
        return True
    else:
        return False

def get_spammer(request):
    global spam_setting
    result = None
    if request in spam_setting:
        index = spam_setting[request]["index"]
        result = spam_setting[request]["list"][index]
        spam_setting[request]["index"] = (index+1) % len(spam_setting[request]["list"])
    return result
