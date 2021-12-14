from settings.all_objects_names_classes_dict import ALL_NAMES_OBJECTS_DICT
from settings.weapon_settings.types_and_names import *
from common_things.common_objects_lists_dicts import *


TYPE_LIST_DICT = {
    BULLETS_TYPE: BULLETS_LIST,
}


def add_object(arena, obj_data):
    obj_global_key = obj_data.get('key')
    if not obj_global_key:
        obj_global_key = int(max(ALL_OBJECT_DICT)) + 1 if ALL_OBJECT_DICT else 1

    obj = ALL_NAMES_OBJECTS_DICT.get(obj_data['name'])(**obj_data['data'], arena=arena)
    obj.KEY = obj_global_key

    collection = TYPE_LIST_DICT[obj.TYPE]
    if type(collection) == set:
        collection.add(obj)
    elif type(collection) == list:
        collection.append(obj)

    ALL_OBJECT_DICT[obj_global_key] = obj

    obj_data['key'] = obj_global_key

    if arena.server_instance:
        arena._new_objects.append(obj_data)