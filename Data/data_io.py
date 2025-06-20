import json

def load_json_data(path):
    with open(path) as f:
        data = json.load(f)
    return data

def write_json_data(data, path):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)