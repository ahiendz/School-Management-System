import json

def load_json_data():
    class_data = []
    with open('data.json') as f:
        data = json.load(f)
    class_data.extend(data)

def write_json_data(data):
    with open('Data\data.json', "w") as f:
        json.dump(data, f, indent=4)