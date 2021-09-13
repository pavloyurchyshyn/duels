from player_and_spells.player.base_player import BasePlayer

from pygame.constants import *
from pygame import key, transform
from pygame.draw import circle, line

from UI.UI_base.animation import Animation
from UI.UI_base.text_UI import Text
from UI.camera import GLOBAL_CAMERA

from math import atan2, cos, sin, degrees, dist

from settings.players_settings.player_settings import *
from settings.screen_size import Y_SCALE, X_SCALE
from settings.global_parameters import GLOBAL_SETTINGS
from settings.colors import BLOOD_COLOR
from settings.window_settings import MAIN_SCREEN
from settings.default_keys import INTERACT_C, \
    UP_C, LEFT_C, RIGHT_C, DOWN_C, \
    SPELL_1_C, SPRINT_C, GRAB_C, DROP_C, RELOAD_C, \
    WEAPON_1_C, WEAPON_2_C, WEAPON_3_C, SELF_DAMAGE
from settings.common_settings import COMMON_GAME_SETTINGS_JSON_PATH as CGSJP

# global things

from common_things.global_clock import ROUND_CLOCK
from common_things.save_and_load_json_config import get_param_from_cgs
from obj_properties.objects_data_creator import objects_data_creator
from player_and_spells.player.player_images import NORMAL_PLAYER_IMGS


class Player(BasePlayer):  # , PhysicalObj):
    MAIN_SCREEN = MAIN_SCREEN
    BLOOD_COLOR = BLOOD_COLOR

    def __init__(self, x, y,
                 arena,
                 size=PLAYER_SIZE,
                 player_color=None,
                 **kwargs):
        super().__init__(x, y, size=size, arena=arena, **kwargs)

        self.color = player_color if player_color else get_param_from_cgs('player_skin', def_value='blue')
        pictures = NORMAL_PLAYER_IMGS.get_new_skin(self.color)
        self.image = pictures['body']
        self.face_anim = Animation(self._center,
                                   idle_frames=pictures['idle_animation'],
                                   **pictures['other_animation'])

        self.camera = kwargs.get('camera', GLOBAL_CAMERA)

        self.hp_text = Text(int(self._health_points), MAIN_SCREEN, x=self._center[0], y=self._center[1] + self._size,
                            auto_draw=False)

        self.hands_radius = 10

    def update(self, commands, mouse, mouse_pos):
        time_d = ROUND_CLOCK.d_time
        self._d_time = time_d
        self._time += time_d

        if self.rotate_to_cursor(mouse_pos, *self.camera.camera) or self.make_step(commands):
            self._make_dots()

        self.camera.update(self._center)

        self.hp_text.change_pos(self._center[0], self._center[1] + self._size)
        self.face_anim.update(d_time=time_d, position=self._center, angle=self._angle)

        self.update_hands_endpoints()

        if mouse[0]:
            self._arena.add_object(objects_data_creator(name='simple_bullet',
                                                        data={
                                                            'x': self._hands_endpoint[0],
                                                            'y': self._hands_endpoint[1],
                                                            'angle': self._angle,
                                                        }))

    def draw(self) -> None:
        dx, dy = self.camera.camera

        x0, y0 = self._center

        img_copy = transform.rotate(self.image, -degrees(self._angle))

        Player.MAIN_SCREEN.blit(img_copy, (x0 - img_copy.get_width() // 2 + dx, y0 - img_copy.get_height() // 2 + dy))

        if self.global_settings['test_draw']:
            for dot in self._dots:
                circle(Player.MAIN_SCREEN, (255, 0, 0), (dot[0] + dx, dot[1] + dy), 3)

        circle(Player.MAIN_SCREEN,
               self.color['body'],
               (self._hands_endpoint[0] + dx, self._hands_endpoint[1] + dy),
               5)

        self.face_anim.draw(dx, dy)
        self.hp_text.draw(dx, dy)

    @property
    def position(self):
        return self._center[0] / X_SCALE, self._center[1] / Y_SCALE

    @position.setter
    def position(self, pos):
        if pos:
            x, y = int(pos[0] * X_SCALE), int(pos[1] * Y_SCALE)
            self._change_position((x, y))

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
