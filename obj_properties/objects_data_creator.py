from settings.all_types_and_names import ALL_OBJ_NAMES
from common_things.common_objects_lists_dicts import ALL_OBJECT_DICT


def objects_data_creator(name, data, key=None):
    if name not in ALL_OBJ_NAMES:
        raise BadObjectName(name=name)

    if key and key in ALL_OBJECT_DICT:
        raise BadObjectKey(key=key)

    return {'name': name, 'data': data, 'key': key}


class BadObjectName(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'Bad object name: {self.name} | {ALL_OBJ_NAMES}'


class BadObjectKey(Exception):
    def __init__(self, key):
        self.key = key

    def __str__(self):
        return f'Bad object key: {self.key}'
