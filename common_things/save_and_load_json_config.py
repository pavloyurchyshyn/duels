import json
from os.path import exists
from common_things.wrappers import memory_keeper


@memory_keeper
def load_json_config(path: str) -> dict:
    if not exists(path):
        return {}

    with open(path, 'r') as k_conf:
        return json.load(k_conf)


def change_parameter_in_json_config(key, value, path):
    j = load_json_config(path)
    j[key] = value
    save_json_config(j, path)


def get_parameter_from_json_config(key, path, def_value=None):
    return load_json_config(path).get(key, def_value)


def save_json_config(data: dict, path: str) -> None:
    with open(path, 'w') as k_conf:
        json.dump(data, k_conf)
