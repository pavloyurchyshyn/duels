from common_things.singletone import Singleton
from common_things.global_clock import ROUND_CLOCK
from common_things.common_objects_lists_dicts import *
from settings.visual_settings.visual_settings import BASE_RECT


class RoundParameters:  # (metaclass=Singleton):
    bullets_list = BULLETS_LIST
    players_list = PLAYERS_DICT
    objects_list = OBJECTS_LIST
    spells_list = SPELLS_LIST

    clock = ROUND_CLOCK

    def __init__(self, ball=None, scores: dict = {}):
        self.arena = BASE_RECT
        self.ball = ball
        self.scores = scores

    def reload(self):
        self.__init__()


GLOBAL_ROUND_PARAMETERS = RoundParameters()
