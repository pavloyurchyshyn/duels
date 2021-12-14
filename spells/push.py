from obj_properties.circle_form import Circle
from common_things.global_clock import ROUND_CLOCK
from spells.base_spell import BaseSpell

from visual.visual_effects_controller import VisualEffectsController
from visual.semi_circle_wave import SemiCircleWave
from common_things.common_objects_lists_dicts import SPELLS_LIST


class PushSpell:
    CD = -1

    def __init__(self, player, clock=ROUND_CLOCK, **kwargs):
        self._clock = clock
        self._owner = player
        self._next_use = 1

    def update(self):
        if self._next_use < 0:
            self._next_use += self._clock.d_time

    def use(self):
        if self._next_use > 0:
            Push(*self._owner._hands_endpoint, self._owner.angle, clock=self._clock)
            self._next_use = PushSpell.CD


class Push(Circle, BaseSpell):

    def __init__(self, x, y, angle, clock):
        super().__init__(x=x, y=y, R=50, dots_angle=1, angle=angle)
        BaseSpell.__init__(self)
        self._clock = clock

        self._size_scale = 33
        self._max_size = 100
        SPELLS_LIST.append(self)

        VisualEffectsController.add_effect(SemiCircleWave(*self._center,
                                                          alive_time=0.25,
                                                          width=5,
                                                          width_scale=-4,
                                                          angle=angle, round_clock=1,
                                                          speed=10,
                                                          )
                                           )

    def interact_with_object(self, obj):
        obj.push(force=50, angle=self._angle)

    def update(self):
        self._size += self._size_scale * self._clock.d_time
        if self._size > self._max_size or self._size < 0:
            self._alive = 0

    @property
    def position(self):
        return self._center
