from interfaces.creature_parts_interfaces import CreatureBrainInterface
from creatures.base_parts.any_part import CreaturePart
from abc import abstractmethod

from common_things.global_clock import GLOBAL_CLOCK, ROUND_CLOCK
from world_arena.world import GLOBAL_WORLD


class BaseBrain(CreatureBrainInterface, CreaturePart):
    WORLD = GLOBAL_WORLD
    G_CLOCK = GLOBAL_CLOCK
    R_CLOCK = ROUND_CLOCK

    def __init__(self, moods: dict, body, base_mood='sleep', hp=100):
        CreaturePart.__init__(self, hp)

        self._max_hp = hp
        self._hp = hp

        self._moods = moods
        self._body = body

        self._current_pattern = moods[base_mood]

        self._alive = 1

    def damage(self, dmg):
        self._hp -= dmg
        if self._hp < 0:
            self._alive = 0

    @abstractmethod
    def _update(self):
        pass

    def set_body(self, body):
        if body != self._body:
            self._body = body

    @property
    def alive(self):
        """
        If brain is dead -> creature dead to

        :return:
        """
        return self._alive
