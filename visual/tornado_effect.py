from obj_properties.base_projectile import Projectile
from visual.base_effect import BaseEffect
from visual.diamond_effect import DiamondEffect
from visual.visual_effects_controller import VisualEffectsController
from math import cos, sin, radians
from obj_properties.rect_form import Rectangle
from settings.window_settings import SCREEN_W, SCREEN_H


class Tornado(Projectile, BaseEffect):

    def __init__(self, x, y,
                 speed=0,
                 angle=0, radius=50,
                 rotate_speed=100, rotate_right=0.1,
                 alive_time=0,
                 sub_effect=None,
                 sub_args=(),
                 sub_kwargs={},
                 arena=Rectangle(0, 0, SCREEN_W, SCREEN_H),
                 color=[255, 255, 255],
                 **kwargs):

        super(Tornado, self).__init__(x=x, y=y, angle=angle, speed=speed, arena=arena, **kwargs)
        BaseEffect.__init__(self, color=color, **kwargs)

        self._radius = radius
        self._rotate_speed = rotate_speed  # radians
        self._rotate_add = radians(rotate_right)

        self._particle_create_delay = 1
        self._alive_time = alive_time
        self._effect = sub_effect if sub_effect else DiamondEffect
        self._effect_args = sub_args
        self._effect_kwargs = sub_kwargs

    def update(self):
        self._update()
        if self._alive_time:
            self._alive_time -= self._d_time

        if self._particle_create_delay < 0:
            self._particle_create_delay += self._d_time
        else:
            self._particle_create_delay = -self._particle_create_delay
            x0, y0 = self._position
            for angle in (radians(0), radians(90), radians(180), radians(270)):
                x = x0 + cos(angle) * self._radius
                y = y0 + sin(angle) * self._radius

                d = self._effect(x=x, y=y,
                                 arena=self.arena,
                                 angle=angle,
                                 angle_change_per_second=self._rotate_add,
                                 *self._effect_args, **self._effect_kwargs
                                 )
                VisualEffectsController.add_effect(d)

    def alive_condition(self):
        return

    def draw(self):
        pass