from obj_properties.base_projectile import Projectile
from settings.visual_settings.effects_types import TRANSPARENT_CIRCLE_TYPE

from common_things.global_clock import GLOBAL_CLOCK
from common_things.img_loader import normalize_color
from common_things.global_round_parameters import GLOBAL_ROUND_PARAMETERS

from pygame import Surface, BLEND_RGB_ADD
from pygame.draw import circle as draw_circle
from visual.base.base_effect import BaseEffect


class TransparentCircle(Projectile, BaseEffect):
    EFFECT_TYPE = TRANSPARENT_CIRCLE_TYPE

    def __init__(self, x, y, angle=0,
                 size=20, size_scale=0,
                 color=[255, 255, 255, 255],
                 arena=None,
                 speed=100,
                 circle_width=0,
                 circle_width_scale=None,
                 alive_condition=None,
                 round_clock=0,
                 transparent=1,
                 **kwargs):
        arena = arena if arena else GLOBAL_ROUND_PARAMETERS.arena

        self.alive_condition = alive_condition if alive_condition else self.__alive_condition

        super(TransparentCircle, self).__init__(x=x, y=y,
                                                angle=angle,
                                                round_clock=round_clock,
                                                speed=speed,
                                                arena=arena,
                                                **kwargs)
        BaseEffect.__init__(self, color=color, **kwargs)

        self._transparent = transparent
        self._data = kwargs
        self._original_size = size
        self._size = size / 2 if transparent else size
        self._half_size = self._size // 2
        self._size_scale = self._size * size_scale
        self._circle_width = circle_width
        self._circle_width_scale = circle_width * circle_width_scale if circle_width_scale else None
        self.draw = self._transparent_draw if transparent else self._draw

    def get_light_surface(self):
        surf = Surface((self._size + self._size, self._size + self._size))
        draw_circle(surf, normalize_color(self._color), (self._size, self._size), self._size, width=int(self._circle_width))
        surf.set_colorkey((0, 0, 0))
        return surf

    def update(self):
        self._clock_dt = dt = GLOBAL_CLOCK.d_time
        self._size += self._size_scale * dt
        if self._circle_width_scale:
            self._circle_width += self._circle_width_scale * dt
            if self._circle_width < 1:
                self._alive = 0
                return

        if self._alive_time:
            self._alive_time -= dt

        self._half_size = self._size // 2
        self._update(delta_time=dt)
        self.update_color()

    def _transparent_draw(self):
        x, y = self.int_position
        dx, dy = self._camera.camera
        img = self.get_light_surface()
        self._screen.blit(img, (x + dx - img.get_width() // 2, y + dy - img.get_height() // 2),
                          special_flags=BLEND_RGB_ADD)

    def _draw(self):
        x, y = self.int_position
        dx, dy = self._camera.camera
        self.DRAW_CIRCLE(self._screen, normalize_color(self._color), (int(x + dx), int(y + dy)), int(self._half_size),
                         width=self._circle_width)

    @staticmethod
    def __alive_condition(self):
        return self._size >= 2 and self.in_arena() and (self._alive_time is None or self._alive_time > 0)
