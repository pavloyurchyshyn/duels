from settings.players_settings.player_settings import *
from settings.players_settings.player_pic_and_anim import get_sprite_and_animations
from obj_properties.circle_form import Circle
from pygame import mouse, transform, draw
from UI.UI_base.animation import Animation

from math import atan2, degrees, sin, cos, dist

from settings.global_parameters import GLOBAL_SETTINGS
from settings.window_settings import MAIN_SCREEN

from UI.camera import GLOBAL_CAMERA
from common_things.global_clock import GLOBAL_CLOCK

from common_things.save_and_load_json_config import get_parameter_from_json_config, change_parameter_in_json_config
from settings.common_settings import COMMON_GAME_SETTINGS_JSON_PATH as CGSJP


class SimplePlayer(Circle):
    MAIN_SCREEN = MAIN_SCREEN

    PLAYER_HP = PLAYER_HP

    def __init__(self, x, y,
                 size=PLAYER_SIZE,
                 player_skin=None,
                 follow_mouse=False,
                 **kwargs):
        super().__init__(x, y, size)

        self._angle = 0
        self.color = player_skin if player_skin else get_parameter_from_json_config('player_skin', CGSJP, def_value='blue')
        pictures = get_sprite_and_animations(self.color, size=(self._size * 2, self._size * 2))
        self.image = pictures['body']
        self.face_anim = Animation(self._center,
                                   idle_frames=pictures['idle_animation'],
                                   **pictures['other_animation'])

        self.turn_off_camera = kwargs.get('turn_off_camera', False)
        # =======================
        # self._full_hp = kwargs.get('hp', Player.PLAYER_HP)
        # self._hp = self._full_hp

        self.camera = kwargs.get('camera', GLOBAL_CAMERA)

        self.global_settings = GLOBAL_SETTINGS

        self.cursor((0, 0))

        self._time = 0.000000001
        self._d_time = 0.00000001
        self.follow_mouse = follow_mouse

        self.arena = None

    def update(self):
        time_d = GLOBAL_CLOCK.d_time

        self._d_time = time_d
        self._time += time_d

        if self.follow_mouse:
            self.cursor(mouse.get_pos())

        self.face_anim.update(time_d, self._center, self._angle)

    def cursor(self, m_pos: tuple):
        x1, y1 = m_pos
        xc, yc = self._center

        if not self.turn_off_camera:
            xc += self.camera.camera[0]
            yc += self.camera.camera[1]
        else:
            xc += 0
            yc += 0

        d_x = 0.00001 if x1 - xc == 0 else x1 - xc
        d_y = 0.00001 if y1 - yc == 0 else y1 - yc

        angle = atan2(d_y, d_x)

        self._angle = angle

    def update_color(self, body_color=None, face_color=None):
        pictures = get_sprite_and_animations((body_color, face_color), size=(self._size, self._size))
        self.image = pictures['body']
        self.face_anim = Animation(self._center,
                                   idle_frames=pictures['idle_animation'],
                                   **pictures['other_animation'])

    def draw(self) -> None:
        # self._messages.draw()
        if self.turn_off_camera:
            dx = dy = 0
        else:
            dx, dy = self.camera.camera

        x0, y0 = self._center

        img_copy = transform.rotate(self.image, -degrees(self._angle))

        SimplePlayer.MAIN_SCREEN.blit(img_copy, (x0 - img_copy.get_width() // 2 + dx, y0 - img_copy.get_height() // 2 + dy))

        if self.global_settings['test_draw']:
            for dot in self._dots:
                draw.circle(SimplePlayer.MAIN_SCREEN, (0, 255, 255), (dot[0] + dx, dot[1] + dy), 1)

        self.face_anim.draw(dx, dy)
        # self.hp_bar.draw()

    @property
    def position(self):
        return self._center

    @position.setter
    def position(self, pos):
        self._change_position(pos)

    @property
    def full_hp(self):
        return self._full_hp

    @full_hp.setter
    def full_hp(self, hp):
        self._full_hp = hp

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value
        # self.hp_bar.update(text=self._hp, current_stage=self._hp, stages_num=self._full_hp)

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value

    def damage(self, damage):
        self._hp -= damage
        # self.hp_bar.update(text=self._hp, current_stage=self._hp, stages_num=self._full_hp)

    @property
    def alive(self):
        return self._hp > 0

    @property
    def dead(self):
        return self._hp <= 0
