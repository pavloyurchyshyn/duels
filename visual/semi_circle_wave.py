# from obj_properties.lazy_load_mixin import PictureLazyLoadMixin
from obj_properties.base_projectile import Projectile
from obj_properties.rect_form import Rectangle
from settings.window_settings import SCREEN_W, SCREEN_H
from visual.base.base_effect import BaseEffect
from math import radians, cos, sin
from pygame.draw import lines as draw_lines
from common_things.img_loader import normalize_color


class SemiCircleWave(Projectile, BaseEffect):
    EFFECT_TYPE = 'semi_circle_wave'
    ANGLES = [radians(angle) for angle in range(-46, 45, 15)]

    def __init__(self, x, y, angle,
                 owner,
                 R=50, size_scale=0,
                 color=[255, 255, 255],
                 arena=Rectangle(0, 0, SCREEN_W, SCREEN_H),
                 speed=500,
                 angles=None,
                 width=1,
                 width_scale=0,
                 alive_time=None,
                 closed =0,
                 **kwargs):
        super(SemiCircleWave, self).__init__(x=x, y=y, angle=angle, speed=speed,
                                             arena=arena, stop_if_out_of_arena=0,
                                             **kwargs)
        BaseEffect.__init__(self, color=color, **kwargs)
        self._r = R
        self._r_scale = R * size_scale
        self._speed += self._r_scale
        self._width = width
        self._closed = closed
        self._width_scale = width * width_scale
        self._dots = []
        self.angles = angles if angles else self.ANGLES
        self._alive_time = alive_time
        self.owner = owner
        self.build_dots()

    def build_dots(self):
        self._dots.clear()
        dx, dy = self._camera.camera
        x0, y0 = self._position
        for angle in self.angles:
            x = x0 + dx
            y = y0 + dy
            c = cos(angle + self._angle)
            s = sin(angle + self._angle)

            x2 = x + c * self._r
            y2 = y + s * self._r
            self._dots.append((x2, y2))
            if self._closed:
                x1 = x + c * (self._r - self._width)
                y1 = y + s * (self._r - self._width)
                self._dots.insert(0, (x1, y1))

    def update(self):
        self._update()
        if self._r_scale:
            self._r -= self._r_scale * self._d_time
        if self._width_scale:
            self._width += self._width_scale * self._d_time
        if self._alive_time:
            self._alive_time -= self._d_time
        self.build_dots()

    def draw(self):
        draw_lines(self._screen, normalize_color(self._color), self._closed, self._dots, width=int(self._width))

    @staticmethod
    def alive_condition(self):
        return self.arena.collide_dots(self) and self._r >= 1 and (self._alive_time is None or self._alive_time > 0)
