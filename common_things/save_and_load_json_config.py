import json
from os.path import exists
from common_things.wrappers import memory_keeper
from settings.common_settings import COMMON_GAME_SETTINGS_JSON_PATH


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


def save_param_to_cgs(key, value):
    change_parameter_in_json_config(key, value, COMMON_GAME_SETTINGS_JSON_PATH)


def get_param_from_cgs(key, def_value=None):
    return get_parameter_from_json_config(key=key, def_value=def_value, path=COMMON_GAME_SETTINGS_JSON_PATH)
