from obj_properties.base_projectile import Projectile
from obj_properties.rect_form import Rectangle
from settings.window_settings import MAIN_SCREEN, SCREEN_W, SCREEN_H

from settings.visual_settings.effects_types import GROWING_LINE_TYPE
from common_things.camera import GLOBAL_CAMERA
from common_things.global_clock import GLOBAL_CLOCK

from math import sin, cos, radians
from pygame.draw import line as draw_line


class GrowingLine(Projectile):
    EFFECT_TYPE = GROWING_LINE_TYPE

    def __init__(self, x, y, angle=0,
                 line_width=1, line_len=100,
                 color=[255, 255, 255, 255],
                 speed=1000,
                 vertical=0,
                 arena=Rectangle(0, 0, SCREEN_W, SCREEN_H),
                 scale_per_sec_k=-1, **kwargs):
        super(GrowingLine, self).__init__(x=x, y=y, angle=angle,
                                          arena=arena, speed=speed,
                                          **kwargs)

        self.line_width = line_width
        self._color = color

        self._line_len = line_len / 2
        self._scale_p_second = self._line_len * scale_per_sec_k

        self._line_dots = ((0, 0), (1, 1))
        self._add_angle = 0.0 if vertical else radians(90)

    def update(self):
        dt = GLOBAL_CLOCK.d_time
        self._update(delta_time=dt)
        self.scale(dt)

        x, y = self.int_position
        dx, dy = GLOBAL_CAMERA.camera

        x0 = x + dx + cos(self._angle + self._add_angle) * self._line_len
        y0 = y + dy + sin(self._angle + self._add_angle) * self._line_len

        x1 = x + dx - cos(self._angle + self._add_angle) * self._line_len
        y1 = y + dy - sin(self._angle + self._add_angle) * self._line_len

        self._line_dots = ((x0, y0), (x1, y1))

    def scale(self, dt):
        self._line_len += self._scale_p_second * dt

    def draw(self):
        draw_line(MAIN_SCREEN, self._color, self._line_dots[0], self._line_dots[1], self.line_width)

    def alive_condition(self):
        return self._line_len >= 1 and self._speed >= 1
