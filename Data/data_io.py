import json
import os

def load_json_data(path):
    if not os.path.exists(path):
        # Nếu file chưa tồn tại, trả về list rỗng
        return []
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json_data(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)