from math import degrees
from pygame import draw, transform

from UI.UI_base.animation import Animation, RotateAnimation

from player.base_visual.player_images import PlayerImagesManager

from settings.network_settings.network_constants import PLAYER_SKIN
from settings.window_settings import MAIN_SCREEN
from settings.colors import PLAYERS_COLORS
from settings.global_parameters import test_draw_status_is_on

from common_things.save_and_load_json_config import get_param_from_cgs
from common_things.global_clock import GLOBAL_CLOCK
from common_things.camera import GLOBAL_CAMERA

from visual.player_effects.hit_blood_drops import player_hit_effect


class PlayerVisualPart:
    screen = MAIN_SCREEN

    def __init__(self, player, player_size, turn_off_camera=0,
                 under_circle=0, under_circle_color=(255, 0, 0),
                 body_color=None, face_color=None,
                 load_angle=90, **kwargs):
        self.body = self.face_animation = self.under_circle = self.heat = None

        self._turn_off_camera = turn_off_camera
        self._under_circle_bool = under_circle

        self._player = player
        self._size = player_size * 2
        self._body_img_size = (self._size, self._size)
        self._circle_size = (int(self._size * 1.1), int(self._size * 1.1))
        self._load_angle = load_angle
        self.img_manager = PlayerImagesManager(size=self._size, angle=self._load_angle, circle_size=self._circle_size)

        self._under_circle_color = under_circle_color
        self._default_colors = get_param_from_cgs(PLAYER_SKIN, PLAYERS_COLORS['blue'])
        self._body_color = body_color if body_color else self._default_colors['body']
        self._face_color = face_color if face_color else self._default_colors['face']

        self.load_new_skin(body_color=self._body_color, face_color=self._face_color)

        self.camera = kwargs.get('camera', GLOBAL_CAMERA)

        self.hit_effect = player_hit_effect

    def load_new_skin(self, body_color, face_color):
        self._body_color = body_color
        self._face_color = face_color

        skin = self.img_manager.get_new_skin((self._body_color, self._face_color))
        self.body = skin.pop('body')
        self.face_animation = Animation(self._player.position,
                                        idle_frames=skin['idle_animation'],
                                        **skin['other_animation'])

        if self._under_circle_bool:
            self.under_circle = self.img_manager.get_circle(self._under_circle_color)

        self.heat = None

    def update(self):
        time_d = GLOBAL_CLOCK.d_time
        self.face_animation.update(time_d, self._player._center, self._player._angle)

    def draw(self) -> None:
        if self._turn_off_camera:
            dx = dy = 0
        else:
            dx, dy = self.camera.camera

        x0, y0 = self._player._center

        main_screen = self.screen
        if self.under_circle:
            self.under_circle.draw(dx=dx, dy=dy)

        img_copy = transform.rotate(self.body, -degrees(self._player._angle))
        main_screen.blit(img_copy, (x0 - img_copy.get_width() // 2 + dx, y0 - img_copy.get_height() // 2 + dy))

        if test_draw_status_is_on():
            for dot in self._player._dots:
                draw.circle(main_screen, (255, 0, 0), (dot[0] + dx, dot[1] + dy), 3)

        draw.circle(main_screen,
                    self._body_color,
                    (self._player._hands_endpoint[0] + dx, self._player._hands_endpoint[1] + dy),
                    3)

        self.face_animation.draw(dx, dy)
