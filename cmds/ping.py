import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from utils.log import FileLogger

class ping:
    def __init__(self):
        self.usage = '!ping'

    def run(self, user_auth, *param):
        if param and len(param[0]) > 0:
            return self.usage