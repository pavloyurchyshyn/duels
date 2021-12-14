from settings.players_settings.player_settings import *
from pygame import mouse, transform, draw

from math import degrees

from settings.global_parameters import GLOBAL_SETTINGS, test_draw_status_is_on  # , X_SCALE, Y_SCALE

from common_things.global_clock import GLOBAL_CLOCK

from settings.default_keys import SPELL_1_C
from player.base_player import BasePlayer


class SimplePlayer(BasePlayer):
    def __init__(self, x, y,
                 arena=None,
                 size=PLAYER_SIZE,
                 follow_mouse=False,
                 **kwargs):
        size = int(size)
        super().__init__(x, y, size=size, arena=arena, load_images=True, **kwargs)
        self.follow_mouse = follow_mouse

        self.global_settings = GLOBAL_SETTINGS

        self.rotate_to_cursor((0, 0))

    def update(self, commands=()):
        time_d = GLOBAL_CLOCK.d_time

        self._d_time = time_d
        self._time += time_d

        self.update_effects(time_d)

        if SPELL_1_C in commands:
            self.face_anim.change_animation('rage')

        if self.follow_mouse:
            mouse_pos = mouse.get_pos()
            c = self.camera.camera
            abs_mouse_pos = mouse_pos[0] - c[0], mouse_pos[1] - c[1]
            self.rotate_to_cursor(abs_mouse_pos)

        self.update_circle_under_player()
        self.update_hands_endpoints()

        self.face_anim.update(time_d, self._center, self._angle)

        self.health_points_text.change_pos(self._center[0], self._center[1] + self._size)

    def update_circle_under_player(self):
        if self.under_player_circle:
            self.under_player_circle.update(self._d_time, position=self._center)

    def _draw(self) -> None:
        if self.turn_off_camera:
            dx = dy = 0
        else:
            dx, dy = self.camera.camera

        x0, y0 = self._center

        main_screen = self.MAIN_SCREEN
        if self.under_player_circle:
            self.under_player_circle.draw(dx=dx, dy=dy)

        img_copy = transform.rotate(self.image, -degrees(self._angle))
        main_screen.blit(img_copy, (x0 - img_copy.get_width() // 2 + dx, y0 - img_copy.get_height() // 2 + dy))

        if test_draw_status_is_on():
            for dot in self._dots:
                draw.circle(main_screen, (255, 0, 0), (dot[0] + dx, dot[1] + dy), 3)

        draw.circle(main_screen,
                    self.color['body'],
                    (self._hands_endpoint[0] + dx, self._hands_endpoint[1] + dy),
                    3)

        self.face_anim.draw(dx, dy)
        if self._draw_health_points:
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
        self.health_points_text.change_text(int(self.health_points))

    def damage(self, damage):
        if damage:
            BasePlayer.damage(self, damage)
            self.health_points_text.change_text(int(self._health_points))
            if self._health_points <= 0.0:
                self.face_anim.change_animation('dying')
            else:
                self.face_anim.change_animation('rage')

    @property
    def position(self):
        # return self._center[0] / X_SCALE, self._center[1] / Y_SCALE
        return self._center[0], self._center[1]

    @position.setter
    def position(self, xy):
        x = xy[0]  # * X_SCALE
        y = xy[1]  # * Y_SCALE
        self._change_position((x, y), True)
