_cmds_registry = {}

def register(cmd:str, alias:str) -> bool:
    if alias in _cmds_registry:
        return False
    else:
        _cmds_registry[alias] = cmd
        return True

def get_cmd(alias:str) -> str:
    if alias in _cmds_registry:
        return _cmds_registry[alias]
    else:
        return ''
