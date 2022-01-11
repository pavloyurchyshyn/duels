from player.base.base_player import BasePlayer
from common_things.global_clock import ROUND_CLOCK
from settings.default_keys import SELF_DAMAGE
from weapons.base.base_range import BaseRange


class NetworkPlayerObject(BasePlayer):
    def __init__(self, x, y,
                 arena,
                 team=None,
                 **kwargs):
        super().__init__(x=x, y=y, team=team, arena=arena,
                         weapon_1=BaseRange(x, y, arena), **kwargs)

    def update(self, commands=(), mouse_buttons=(0, 0, 0), mouse_pos=None):
        time_d = ROUND_CLOCK.d_time
        self._d_time = time_d
        self._time += time_d

        self.update_effects(time_d)
        self.make_step(commands)

        self.update_hands_endpoints()
        self.update_weapon()

        if SELF_DAMAGE in commands:
            self.damage(5)

        self.check_for_bullets_interaction()

        self.use_self_force()
        c = self.camera.camera
        abs_mouse_pos = mouse_pos[0] - c[0], mouse_pos[1] - c[1]
        self.rotate_to_cursor(abs_mouse_pos)
        self.make_step(commands)

        self.update_hands_endpoints()
        self.check_for_weapon_switch(commands)

        self.update_weapon()
        self.update_spells()

        self.use_spells(commands)

        if mouse_buttons[0]:
            self.use_weapon()
        elif mouse_buttons[2]:
            self.alt_use_weapon()

        self._make_dots()
