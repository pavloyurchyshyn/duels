from player.base_player import BasePlayer

from pygame import transform
from pygame.draw import circle

from math import degrees

from settings.players_settings.player_settings import *
from settings.global_parameters import test_draw_status_is_on

# global things

from common_things.global_clock import ROUND_CLOCK
from obj_properties.objects_data_creator import objects_data_creator
from settings.default_keys import SPELL_1_C, SPELL_2_C
from weapons.base.base_range import BaseRange
from spells.teleport import Teleport
from spells.push import PushSpell


class Player(BasePlayer):
    def __init__(self, x, y,
                 arena,
                 size=PLAYER_SIZE,
                 **kwargs):

        super().__init__(x, y, size=size, arena=arena, load_images=True,
                         spell_1=PushSpell, spell_3=Teleport,
                         weapon_1=BaseRange(x, y, arena),
                         **kwargs)

    def update(self, commands=(), mouse=(0, 0, 0), mouse_pos=None):
        time_d = ROUND_CLOCK.d_time
        self._d_time = time_d
        self._time += time_d

        self.use_self_force()
        c = self.camera.camera
        abs_mouse_pos = mouse_pos[0] - c[0], mouse_pos[1] - c[1]
        self.rotate_to_cursor(abs_mouse_pos)
        self.make_step(commands)

        self.health_points_text.change_pos(self._center[0], self._center[1] + self._size)
        self.face_anim.update(d_time=time_d, position=self._center, angle=self._angle)

        self.update_hands_endpoints()
        self.check_for_weapon_switch(commands)

        self.update_weapon()
        self.update_spells()

        self.use_spells(commands)

        if mouse[0]:
            self.use_weapon()
        elif mouse[2]:
            self.alt_use_weapon()

        self._make_dots()

    def _draw(self) -> None:
        dx, dy = self.camera.camera

        x0, y0 = self._center

        main_screen = self.MAIN_SCREEN

        img_copy = transform.rotate(self.image, -degrees(self._angle))
        main_screen.blit(img_copy, (x0 - img_copy.get_width() // 2 + dx, y0 - img_copy.get_height() // 2 + dy))

        if test_draw_status_is_on():
            for dot in self._dots:
                circle(main_screen, (255, 0, 0), (dot[0] + dx, dot[1] + dy), 3)

        circle(main_screen,
               self.color['body'],
               (self._hands_endpoint[0] + dx, self._hands_endpoint[1] + dy),
               5)

        self.face_anim.draw(dx, dy)
        self.health_points_text.draw(dx, dy)

        for item in self._weapon.values():
            if item:
                item.draw()

    @property
    def position(self):
        # return self._center[0] / X_SCALE, self._center[1] / Y_SCALE
        return self._center

    @position.setter
    def position(self, pos):
        if pos:
            # x, y = int(pos[0] * X_SCALE), int(pos[1] * Y_SCALE)
            self._change_position(pos)

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
                self.face_anim.change_animation('idle')

            self._health_points = health_points
            self.hp_text.change_text(int(health_points))

    def revise(self):
        self._health_points = self._full_health_points
        self.face_anim.change_animation('idle')

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
            self.hp_text.change_text(int(self._health_points))
            if self._health_points <= 0.0:
                self.face_anim.change_animation('dying')
            else:
                self.face_anim.change_animation('rage')
        # self.hp_bar.update(text=self._hp, current_stage=self._hp, stages_num=self._full_hp)
