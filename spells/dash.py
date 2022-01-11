from spells.base_spell import BaseSpellProjectile, SpellIcon
from common_things.global_clock import ROUND_CLOCK


class DashSpell(SpellIcon):
    CD = -0.5
    PUSH_FORCE = 2000

    def __init__(self, owner, clock=ROUND_CLOCK, **kwargs):
        super().__init__()
        self._clock = clock
        self._owner = owner
        self._next_use = 1

    def update(self):
        if self._next_use < 0:
            self._next_use += self._clock.d_time

    def use(self):
        if self._next_use > 0:
            self._owner.push(pos=self._owner._dots[7], force=self.PUSH_FORCE)
            self._next_use = DashSpell.CD

    @property
    def cooldown(self):
        return self._next_use

    @property
    def on_cooldown(self):
        return self._next_use < 0.0
