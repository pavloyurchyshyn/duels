from settings.players_settings.player_settings import *
from pygame import mouse, transform, draw

from math import degrees

from settings.global_parameters import GLOBAL_SETTINGS, test_draw_status_is_on

from common_things.global_clock import GLOBAL_CLOCK
from common_things.camera import GLOBAL_CAMERA

from player.base.base_player import BasePlayer
from player.base.player_with_pictures import PlayerLazyLoad


class SimplePlayer(BasePlayer, PlayerLazyLoad):
    def __init__(self, x, y,
                 arena=None,
                 size=PLAYER_SIZE,
                 follow_mouse=False,
                 **kwargs):
        size = int(size)
        super().__init__(x, y, size=size, arena=arena, **kwargs)
        PlayerLazyLoad.__init__(self)
        self.img_size = size, size
        self.follow_mouse = follow_mouse
        self.camera = kwargs.get('camera', GLOBAL_CAMERA)
        self.global_settings = GLOBAL_SETTINGS

        self.rotate_to_cursor((0, 0))

    def update(self, commands=()):
        time_d = GLOBAL_CLOCK.d_time

        self._d_time = time_d
        self._time += time_d

        self.update_effects(time_d)

        if self.follow_mouse:
            mouse_pos = mouse.get_pos()
            c = self.camera.camera
            abs_mouse_pos = mouse_pos[0] - c[0], mouse_pos[1] - c[1]
            self.rotate_to_cursor(abs_mouse_pos)

        # self.update_circle_under_player()
        self.update_hands_endpoints()

        self._visual_part.update()

    #         self.health_points_text.change_pos(self._center[0], self._center[1] + self._size)

    def update_circle_under_player(self):
        if self.under_player_circle:
            self.under_player_circle.update(self._d_time, position=self._center)

    def draw(self) -> None:
        if self._visual_part:
            self._visual_part.draw()

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

    #       self.health_points_text.change_text(int(health_points))

    def revise(self):
        BasePlayer.revise(self)
        self.face_anim.change_animation('idle')

    #        self.health_points_text.change_text(int(self.health_points))

    def damage(self, damage):
        if damage:
            BasePlayer.damage(self, damage)
            #             self.health_points_text.change_text(int(self._health_points))
            if self._health_points <= 0.0:
                self.face_anim.change_animation('dying')
            else:
                self.face_anim.change_animation('rage')

    @property
    def position(self):
        return self._center[0], self._center[1]

    @position.setter
    def position(self, xy):
        self._change_position(xy, 1)
