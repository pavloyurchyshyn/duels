from common_things.singletone import Singleton
from common_things.global_clock import ROUND_CLOCK
from common_things.common_objects_lists_dicts import *
from settings.visual_settings.visual_settings import BASE_RECT


class RoundParameters1:  # (metaclass=Singleton):
    bullets_list = BULLETS_LIST
    players_list = PLAYERS_LIST
    objects_list = OBJECTS_LIST
    spells_list = SPELLS_LIST

    clock = ROUND_CLOCK

    def __init__(self):
        self.arena = BASE_RECT
        self.ball = None

    def reload(self):
        self.__init__()


GLOBAL_ROUND_PARAMETERS = RoundParameters1()
