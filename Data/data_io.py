import json

def load_json_data(path):
    with open(path, 'r',encoding="utf-8") as f:
        data = json.load(f)
    return data

def write_json_data(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)