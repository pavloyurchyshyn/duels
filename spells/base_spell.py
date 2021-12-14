from common_things.common_objects_lists_dicts import SPELLS_LIST


class BaseSpell:
    def __init__(self):
        self._alive = 1
        SPELLS_LIST.append(self)

    @property
    def alive(self):
        return self._alive

    @property
    def dead(self):
        return not self._alive