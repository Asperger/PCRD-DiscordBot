import os.path as path
import json


def get_token():
    token_path = path.join(path.dirname(__file__), 'token.json')
    with open(token_path) as json_file:
        data = json.load(json_file)
        return data['token']


if __name__ == '__main__':
    print(get_token())
