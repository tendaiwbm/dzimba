import json

def read_json(filepath):
    with open(filepath,"r") as f:
        return json.load(f)
