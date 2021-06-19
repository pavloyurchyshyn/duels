import json


def load_json_config(path: str) -> dict:
    with open(path, 'r') as k_conf:
        return json.load(k_conf)


def save_json_config(data: dict, path: str) -> None:
    with open(path, 'w') as k_conf:
        json.dump(data, k_conf)