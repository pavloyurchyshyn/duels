from player.base.player_with_pictures import PlayerLazyLoad
from player.base.base_player import BasePlayer
from pygame.draw import circle

from math import degrees

from settings.players_settings.player_settings import *
from settings.global_parameters import test_draw_status_is_on

# global things

from common_things.global_clock import ROUND_CLOCK
from settings.default_keys import SELF_DAMAGE, SELF_REVISE
from weapons.base.base_range import BaseRange
from weapons.base.base_melee import BaseMelee
from spells.teleport import Teleport
from spells.push import PushSpell
from spells.dash import DashSpell


class Player(BasePlayer, PlayerLazyLoad):
    def __init__(self, x, y,
                 arena,
                 size=PLAYER_SIZE,
                 **kwargs):

        super().__init__(x, y, size=size, arena=arena, load_images=True,
                         spell_1=PushSpell, spell_2=DashSpell, spell_3=Teleport,
                         weapon_1=BaseRange, weapon_2=BaseMelee, **kwargs)
        PlayerLazyLoad.__init__(self, **kwargs)

    def update(self, commands=(), mouse=(0, 0, 0), mouse_pos=None):
        time_d = ROUND_CLOCK.d_time
        self._d_time = time_d
        self._time += time_d

        self.use_self_force()
        c = self.camera.camera
        abs_mouse_pos = mouse_pos[0] - c[0], mouse_pos[1] - c[1]

        self.rotate_to_cursor(abs_mouse_pos)
        self.make_step(commands)
        self._make_dots()

        self.update_hands_endpoints()
        self.check_for_weapon_switch(commands)

        self.update_weapon()
        self.update_spells()

        self.use_spells(commands)

        if SELF_DAMAGE in commands:
            self.damage(5)

        if SELF_REVISE in commands:
            self.revise()

        if mouse[0]:
            self.use_weapon()
        elif mouse[2]:
            self.alt_use_weapon()


        if self._visual_part:
            self._visual_part.update()

    def draw(self) -> None:
        if self._visual_part:
            self._visual_part.draw()

        for item in self._weapon.values():
            if item and item != self._active_weapon:
                item.draw()

    @property
    def health_points(self):
        return self._health_points

    @health_points.setter
    def health_points(self, health_points):
        if health_points is not None:
            if self._health_points < health_points:
                pass
                # TODO heal animation
            elif self._health_points > 0.0:
                if self._visual_part:
                    self._visual_part.face_animation.change_animation('idle')

            self._health_points = health_points
            # self.health_points_text.change_text(int(health_points))

    def revise(self):
        self._health_points = self._full_health_points
        # self.health_points_text.change_text(self._health_points)
        if self._visual_part:
            self._visual_part.face_animation.change_animation('idle')

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        if value:
            self._angle = value

    def damage(self, damage):
        if damage:
            self._health_points -= damage
            if self._health_points <= 0.0:
                if self._visual_part:
                    self._visual_part.face_animation.change_animation('dying')
            else:
                if self._visual_part:
                    self._visual_part.face_animation.change_animation('rage')
