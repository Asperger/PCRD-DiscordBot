import collections
from threading import Lock
from os.path import exists

from utils.log import FileLogger
from utils.reserved import reserved
from collections import deque

class BackupDict(collections.MutableMapping):
    def __init__(self, *args, **kwargs):
        self._store = dict()
        self._lock = Lock()
        self._store_path = ''
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        return self._store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self._store[self.__keytransform__(key)] = value

    def __delitem__(self, key):
        del self._store[self.__keytransform__(key)]

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def __keytransform__(self, key):
        return key

    def __del__(self): 
        self.backup()
        del self._store

    def backup(self):
        result = False
        with self._lock:
            with open(self._store_path, 'w', encoding="utf-8") as f:
                try:
                    f.write(repr(self._store))
                    result = True
                except Exception as e:
                    FileLogger.error(f'Fail to write dictionary: {str(e)}')
        return result

    def setpath(self, path:str) -> bool:
        result = False
        self._store_path = path
        if exists(path):
            with open(path, 'r', encoding="utf-8") as f:
                spam_setting_str = f.read()
                if spam_setting_str:
                    try:
                        self._store = eval(spam_setting_str)
                        result = True
                    except Exception as e:
                        FileLogger.error(f'Fail to read dictionary: {str(e)}')
                        self._store = dict()
        return result
