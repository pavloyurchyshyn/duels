from obj_properties.circle_form import Circle
from common_things.global_clock import ROUND_CLOCK
from spells.base_spell import BaseSpellProjectile, SpellIcon

from visual.base.visual_effects_controller import VisualEffectsController
from visual.semi_circle_wave import SemiCircleWave
from common_things.common_objects_lists_dicts import SPELLS_LIST


class PushSpell(SpellIcon):
    CD = -1

    def __init__(self, owner, clock=ROUND_CLOCK, **kwargs):
        super().__init__()
        self._clock = clock
        self._owner = owner
        self._next_use = 1
        self._d_time = self._clock.d_time

    def update(self):
        if self._next_use < 0:
            self._next_use += self._clock.d_time
            self._d_time = self._clock.d_time

    def use(self):
        if self._next_use > 0:
            Push(*self._owner._hands_endpoint, self._owner.angle, clock=self._clock, owner=self._owner)
            self._next_use = PushSpell.CD

    @property
    def cooldown(self):
        return self._next_use

    @property
    def on_cooldown(self):
        return self._next_use < 0.0


class Push(Circle, BaseSpellProjectile):

    def __init__(self, x, y, angle, clock, owner):
        super().__init__(x=x, y=y, R=50, dots_angle=1, angle=angle)
        BaseSpellProjectile.__init__(self)

        self._clock = clock
        self.owner = owner
        self._size_scale = 33
        self._max_size = 100
        self._d_time = self._clock.d_time

        SPELLS_LIST.append(self)

        VisualEffectsController.add_effect(SemiCircleWave(*self._center,
                                                          owner=self.owner,
                                                          alive_time=0.25,
                                                          width=5,
                                                          width_scale=-4,
                                                          angle=angle, round_clock=1,
                                                          speed=10,
                                                          )
                                           )

    def interact_with_player(self, player):
        player.push(force=5000*self._d_time, angle=self._angle)

    def interact_with_object(self, obj):
        obj.push(force=5000*self._d_time, angle=self._angle)

    def update(self):
        self._size += self._size_scale * self._clock.d_time
        self._d_time = self._clock.d_time

        self.check_for_players_intersection()
        self.check_for_objects_intersection()

        if self._size > self._max_size or self._size < 0:
            self._alive = 0

    @property
    def position(self):
        return self._center
