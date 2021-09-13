from settings.players_settings.player_settings import *
from settings.network_settings.network_constants import PLAYER_SKIN
from pygame import mouse, transform, draw
from UI.UI_base.animation import Animation, RotateAnimation

from math import atan2, degrees, sin, cos, dist, radians

from settings.global_parameters import GLOBAL_SETTINGS
from settings.window_settings import MAIN_SCREEN

from UI.camera import GLOBAL_CAMERA
from UI.UI_base.text_UI import Text
from common_things.global_clock import GLOBAL_CLOCK
from common_things.save_and_load_json_config import get_param_from_cgs

from player_and_spells.player.player_images import NORMAL_PLAYER_IMGS, PlayerImagesManager
from settings.default_keys import INTERACT_C, \
    UP_C, LEFT_C, RIGHT_C, DOWN_C, \
    SPELL_1_C, SPRINT_C, GRAB_C, DROP_C, RELOAD_C, \
    WEAPON_1_C, WEAPON_2_C, WEAPON_3_C, SELF_DAMAGE
from player_and_spells.player.base_player import BasePlayer


class SimplePlayer(BasePlayer):
    PLAYER_HP = PLAYER_HEALTH_POINTS
    CIRCLE_ROT_SPEED = 0.01
    MAIN_SCREEN = MAIN_SCREEN

    def __init__(self, x, y,
                 arena=None,
                 size=PLAYER_SIZE,
                 player_skin=None,
                 follow_mouse=False,
                 under_circle_color=None,
                 **kwargs):
        size = int(size)
        super().__init__(x, y, size=size, arena=arena)
        self.turn_off_camera = kwargs.get('turn_off_camera', False)
        self.follow_mouse = follow_mouse

        self.color = player_skin if player_skin else get_param_from_cgs(PLAYER_SKIN, def_value='blue')

        self.images_manager = NORMAL_PLAYER_IMGS if size == PLAYER_SIZE else PlayerImagesManager(size=size)

        pictures = self.images_manager.get_new_skin(self.color)
        self.image = pictures['body']
        self.face_anim = Animation(self._center,
                                   idle_frames=pictures['idle_animation'],
                                   **pictures['other_animation'])

        self.under_player_circle = RotateAnimation(self._center, self.images_manager.get_circle()) if under_circle_color else None

        self.camera = kwargs.get('camera', GLOBAL_CAMERA)

        self.global_settings = GLOBAL_SETTINGS

        self.rotate_to_cursor((0, 0))

        self.arena = arena
        self.__draw_health_points = kwargs.get('draw_health_points', True)
        self.health_points_text = Text(int(self._health_points), MAIN_SCREEN, x=self._center[0],
                                       y=self._center[1] + self._size,
                                       auto_draw=False)

    def update(self, commands=()):
        time_d = GLOBAL_CLOCK.d_time

        self._d_time = time_d
        self._time += time_d

        if SPELL_1_C in commands:
            self.face_anim.change_animation('rage')

        if self.follow_mouse:
            self.rotate_to_cursor(mouse.get_pos(), *(0, 0) if self.turn_off_camera else self.camera.camera)

        self.update_circle_under_player()
        self.update_hands_endpoints()

        self.face_anim.update(time_d, self._center, self._angle)

        self.health_points_text.change_pos(self._center[0], self._center[1] + self._size)

    def update_circle_under_player(self):
        if self.under_player_circle:
            self.under_player_circle.update(self._d_time, position=self._center)

    def update_color(self, body_color=None, face_color=None):
        pictures = self.images_manager.get_new_skin((body_color, face_color))
        self.image = pictures['body']
        self.face_anim = Animation(self._center,
                                   idle_frames=pictures['idle_animation'],
                                   **pictures['other_animation'])

    def draw(self) -> None:
        if self.turn_off_camera:
            dx = dy = 0
        else:
            dx, dy = self.camera.camera

        x0, y0 = self._center

        main_screen = SimplePlayer.MAIN_SCREEN
        if self.under_player_circle:
            self.under_player_circle.draw(dx=dx, dy=dy)

        img_copy = transform.rotate(self.image, -degrees(self._angle))

        main_screen.blit(img_copy, (x0 - img_copy.get_width() // 2 + dx, y0 - img_copy.get_height() // 2 + dy))

        if self.global_settings['test_draw']:
            for dot in self._dots:
                draw.circle(main_screen, (255, 0, 0), (dot[0] + dx, dot[1] + dy), 3)

        draw.circle(main_screen,
                    self.color['body'],
                    (self._hands_endpoint[0] + dx, self._hands_endpoint[1] + dy),
                    3)

        self.face_anim.draw(dx, dy)
        if self.__draw_health_points:
            self.health_points_text.draw(dx, dy)

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
            self.health_points_text.change_text(int(health_points))

    def revise(self):
        BasePlayer.revise(self)
        self.face_anim.change_animation('idle')

    def damage(self, damage):
        if damage:
            BasePlayer.damage(self, damage)
            self.health_points_text.change_text(int(self._health_points))
            if self._health_points <= 0.0:
                self.face_anim.change_animation('dying')
            else:
                self.face_anim.change_animation('rage')
