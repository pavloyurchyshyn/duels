from settings.weapon_settings.types_and_names import *
from settings.spells_settings.spells_constants import SPELL_TYPE
from settings.global_parameters import its_client_instance

from common_things.singletone import Singleton
from common_things.all_objects_names_classes_dict import *
from common_things.common_objects_lists_dicts import *
from common_things.global_round_parameters import GLOBAL_ROUND_PARAMETERS
from common_things.loggers import LOGGER


class AllObjectsController(metaclass=Singleton):
    """
    Carrying creating of all spells, objects, bullets, melee hits
    """

    TYPE_LIST_DICT = {
        BULLETS_TYPE: BULLETS_LIST,
        MELEE_HIT_TYPE: MELEE_HITS_LIST,
        SPELL_TYPE: SPELLS_LIST,
        OBJECT_TYPE: OBJECTS_LIST
    }

    def __init__(self, arena=None):
        self._client_instance = its_client_instance()
        self._server_instance = not its_client_instance()

        self._players_dict = PLAYERS_DICT

        self._hits_list = MELEE_HITS_LIST
        self._bullets_list = BULLETS_LIST
        self._objects_list = OBJECTS_LIST
        self._spells_list = SPELLS_LIST

        self._new_objects_data = NEW_OBJECTS_KEYS
        self._dead_objects_keys = DEAD_OBJECTS_KEYS

        # Dict which contains all objects like id: object
        self._all_objects_dict = ALL_OBJECT_DICT

        self._round_parameters = GLOBAL_ROUND_PARAMETERS
        self._network_dead_objects_keys = []
        self._round_clock = self._round_parameters.clock

        self._id_counter = 1

    def get_obj_id(self):
        self._id_counter += 1
        return self._id_counter

    def get_player_by_id(self, id):
        owner = self._players_dict.get(id)
        if owner:
            return owner
        else:
            return id

    def update(self):
        draw = self._client_instance
        for obj in self._objects_list.copy():
            obj.update()
            if obj.dead:
                self._dead_objects_keys.add(obj.GLOBAL_KEY)
            elif draw:
                obj.draw()

        for spell in self._spells_list.copy():
            spell.update()
            if spell.dead:
                self._dead_objects_keys.add(spell.GLOBAL_KEY)
            elif draw:
                spell.draw()

        for bullet in self._bullets_list.copy():
            bullet.update()
            if bullet.dead:
                self._dead_objects_keys.add(bullet.GLOBAL_KEY)
            elif draw:
                bullet.draw()

        for hit in MELEE_HITS_LIST.copy():
            hit.update()
            if hit.dead:
                MELEE_HITS_LIST.remove(hit)

        if not draw:
            self._network_dead_objects_keys.extend(self._dead_objects_keys)

        while self._dead_objects_keys:
            self.delete_object_by_key(obj_key=self._dead_objects_keys.pop())

    def delete_object_by_key(self, obj_key):
        if obj_key in self._all_objects_dict:
            obj = self._all_objects_dict.pop(obj_key)
            self.TYPE_LIST_DICT[obj.OBJ_TYPE].remove(obj)

    def add_object(self, obj_data: dict):
        LOGGER.info(f'Object creating: {obj_data}')
        # unique id for each object
        obj_global_key = obj_data['key'] if obj_data.get('key') else self.get_obj_id()
        self.is_name_and_key_valid(name=obj_data['name'], key=obj_global_key)

        obj_data['data']['owner'] = self.get_player_by_id(obj_data['data']['owner'])
        obj_data['data']['clock'] = self._round_clock
        obj = ALL_NAMES_OBJECTS_DICT[obj_data['name']](**obj_data['data'], arena=self._round_parameters.arena)
        # print(obj)
        obj.GLOBAL_KEY = obj_global_key

        self.TYPE_LIST_DICT[obj.OBJ_TYPE].append(obj)
        self._all_objects_dict[obj_global_key] = obj

        LOGGER.info(f'Object created: {obj_global_key} - {obj_data}')
        if self._server_instance:
            obj_data['key'] = obj_global_key
            self._new_objects_data.append(obj_data)

    def is_name_and_key_valid(self, name, key=None):
        if name not in ALL_OBJ_NAMES:
            raise BadObjectName(name=name)

        if key and key in ALL_OBJECT_DICT:
            raise BadObjectKey(key=key)

    def get_net_new_objects_keys(self):
        l = self._new_objects_data.copy()
        self._new_objects_data.clear()
        return l

    def get_net_dead_objects_keys(self):
        l = self._dead_objects_keys.copy()
        self._dead_objects_keys.clear()
        return l

    def clear(self):
        for collection in (self._bullets_list, self._players_dict, self._objects_list,
                           self._spells_list, self._hits_list, self._all_objects_dict ):
            collection.clear()

# def add_object(arena, obj_data):
#     obj_global_key = obj_data.get('key')
#     if not obj_global_key:
#         obj_global_key = str(int(max(ALL_OBJECT_DICT)) + 1) if ALL_OBJECT_DICT else '1'
#
#     obj = ALL_NAMES_OBJECTS_DICT.get(obj_data['name'])(**obj_data['data'], arena=arena)
#     obj.KEY = obj_global_key
#
#     collection = TYPE_LIST_DICT[obj.OBJ_TYPE]
#     if type(collection) == set:
#         collection.add(obj)
#     elif type(collection) == list:
#         collection.append(obj)
#
#     ALL_OBJECT_DICT[obj_global_key] = obj
#
#     obj_data['key'] = obj_global_key
#
#     if arena.server_instance:
#         arena._new_objects.append(obj_data)


class BadObjectName(Exception):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'Bad object name: {self.name} | Doest`n exists in {ALL_OBJ_NAMES}'


class BadObjectKey(Exception):
    def __init__(self, key):
        self.key = key

    def __str__(self):
        return f'Bad object key: {self.key}'
