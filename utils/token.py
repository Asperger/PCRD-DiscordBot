import os
import json

def get_token():
    token_path = os.path.join(os.path.dirname(__file__),'token.json')
    with open(token_path) as json_file:
        data = json.load(json_file)
        return data['token']