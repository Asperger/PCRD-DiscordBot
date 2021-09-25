from os.path import dirname, join
from json import load

def get_token():
    token_path = join(dirname(__file__), 'token.json')
    with open(token_path) as json_file:
        data = load(json_file)
        return data['token']