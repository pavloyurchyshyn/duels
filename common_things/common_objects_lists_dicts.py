"""

GLOBAL lists/sets of objects for easy access.

"""
from numpy import array, append, insert, delete, copy, where, ndenumerate, nditer


class NumList:
    def __init__(self):
        self._list = array([])

    def append(self, value):
        self._list = append(self._list, value)

    def remove(self, element):
        self._list = delete(self._list, where(self._list == element))

    def __len__(self):
        return len(self._list)

    def copy(self):
        return copy(self._list)

    def __iter__(self):
        # print(i for i in ndenumerate(self._list))
        return map(lambda a: a[1], ndenumerate(self._list))

    def clear(self):
        self._list = array([])


PARTICLE_LIST_L1 = []  # NumList()
PARTICLE_LIST_L0 = []  # NumList()
BULLETS_LIST = []  # NumList()
SPELLS_LIST = []
MELEE_HITS_LIST = []
OBJECTS_LIST = []
PLAYERS_LIST = []


NEW_OBJECTS = []
DEAD_OBJECTS = []

ALL_OBJECT_DICT = {}
