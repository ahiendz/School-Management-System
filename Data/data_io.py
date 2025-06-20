import json

def load_json_data():
    with open('Data\data.json') as f:
        data = json.load(f)
    return data

def write_json_data(data):
    with open('Data\data.json', "w") as f:
        json.dump(data, f, indent=4)