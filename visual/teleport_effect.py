from visual.base.visual_effects_controller import VisualEffectsController
from visual.base.base_effect import BaseEffect
from visual.base.transparent_circle_effect import TransparentCircle
from common_things.common_functions import get_angle_between_dots
from common_things.global_clock import GLOBAL_CLOCK, ROUND_CLOCK
from math import radians, cos, sin

from random import randrange, random
from random import choice as random_choice


def alive_con(self):
    self._live_time -= self._clock.d_time
    return self._live_time > 0


class TeleportEffect(BaseEffect):
    EFFECT_TYPE = 'teleport_effect'

    PARTICLES_COLORS = ([0, 0, 255], [255, 25, 255], [0, 0, 255], [155, 25, 255], [110, 110, 255])
    PARTICLES_COLOR_CHANGE = [0, 0, 255]

    UNDER_PARTICLE_LIGHT_COLOR = [100, 100, 200]
    UNDER_PARTICLE_LIGHT_COLOR_CHANGE = [255, 255, 200]

    ANGLES = [radians(angle) for angle in range(0, 360, 10)]

    def __init__(self, start_position,
                 dest_position,
                 round_clock=1,
                 radius=10,
                 arena=None,
                 **kwargs
                 ):
        self._clock = ROUND_CLOCK if round_clock else GLOBAL_CLOCK

        super(TeleportEffect, self).__init__(round_clock=round_clock, **kwargs)

        self._start_pos = start_position
        self._dest_pos = dest_position

        self._radius = radius

        self._angle = get_angle_between_dots(self._dest_pos, self._start_pos)

        self._dots_pos = self._start_pos[0] + cos(self._angle) * self._radius * 10, self._start_pos[1] + sin(
            self._angle) * self._radius * 10

        self._next_create = 1
        self._particles_create_delay = 1

        self._clock_int = round_clock
        self._alive_time = 5
        self._arena = arena

    def update(self):
        self._alive_time -= self._clock.d_time
        if self._next_create < 0:
            self._next_create += self._clock.d_time
        else:
            x1, y1 = self._start_pos
            for angle in self.ANGLES:
                # x = x1 + cos(angle) * randrange(0, self._radius)
                # y = y1 + sin(angle) * randrange(0, self._radius)

                angle_ = get_angle_between_dots(self._dots_pos, (x1, y1))

                VisualEffectsController.add_effect(TransparentCircle(x=x1, y=y1,
                                                                     size=randrange(5, 10),
                                                                     speed=randrange(150, 260),
                                                                     angle=angle_ + radians(randrange(-25, 25)),
                                                                     color=random_choice(self.PARTICLES_COLORS).copy(),
                                                                     transparent=0,
                                                                     color_change=(255, 255, 255),
                                                                     size_scale=-random() - 0.5,
                                                                     arena=self._arena,
                                                                     ),
                                                   layer=0)

                # VisualEffectsController.add_effect(TransparentCircle(x=x, y=y,
                #                                                      size=randrange(5, 10),
                #                                                      speed=randrange(100, 210),
                #                                                      angle=angle_ + radians(randrange(-25, 25)),
                #                                                      color=random_choice(self.PARTICLES_COLORS).copy(),
                #                                                      transparent=0,
                #                                                      color_change=(255, 255, 255),
                #                                                      size_scale=-random() - 0.5,
                #                                                      ),
                #                                    layer=1)

                VisualEffectsController.add_effect(TransparentCircle(*self._dest_pos,
                                                                     size=randrange(3, 7),
                                                                     speed=randrange(50, 100),
                                                                     angle=angle,
                                                                     color=random_choice(self.PARTICLES_COLORS).copy(),
                                                                     transparent=0,
                                                                     color_change=(255, 255, 255),
                                                                     size_scale=-random() - 0.1,
                                                                     ),
                                                   layer=0)

    def draw(self):
        pass  # draw_circle(self._screen, (0, 0, 255), self._dots_pos, 5)

    @property
    def dead(self):
        return self._alive_time > 0


class RedTeleportEffect(TeleportEffect):
    PARTICLES_COLORS = ([255, 0, 0], [255, 25, 155], [255, 20, 55], [155, 25, 55], [255, 110, 110])
    PARTICLES_COLOR_CHANGE = [255, 0, 0, ]

    UNDER_PARTICLE_LIGHT_COLOR = [100, 100, 200]
    UNDER_PARTICLE_LIGHT_COLOR_CHANGE = [255, 255, 200]
