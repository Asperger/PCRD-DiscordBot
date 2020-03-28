_func_registry = []

def register(func):
    _func_registry.append(func)

def execute():
    return [f() for f in _func_registry]