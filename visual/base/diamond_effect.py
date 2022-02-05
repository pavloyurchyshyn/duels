from obj_properties.base_projectile import Projectile
from settings.visual_settings.diamond_effect import *
from settings.visual_settings.effects_types import DIAMOND_TYPE
from settings.visual_settings.visual_settings import BASE_RECT
from math import cos, sin
from common_things.global_round_parameters import GLOBAL_ROUND_PARAMETERS
from common_things.img_loader import normalize_color

from visual.base.base_effect import BaseEffect


class DiamondEffect(Projectile, BaseEffect):
    EFFECT_TYPE = DIAMOND_TYPE
    MEMBERED_SPRITES = {}

    def __init__(self, x, y, speed=100, angle=0,
                 scale_per_second=(0, 0, 0),
                 tail_len=TAIL_LEN,
                 head_len=HEAD_LEN,
                 width_len=WIDTH_LEN,
                 live_time=None,
                 fill_form=0,
                 lines_width=5,
                 lighting=0,
                 round_clock=0,
                 color=[255, 255, 255, 255],
                 color_change=None,
                 arena=None,
                 **kwargs):
        arena = arena if arena else GLOBAL_ROUND_PARAMETERS.arena
        super(DiamondEffect, self).__init__(x=x, y=y,
                                            speed=speed, angle=angle,
                                            round_clock=round_clock,
                                            arena=arena,
                                            **kwargs)
        BaseEffect.__init__(self, color=color,
                            color_change=color_change, **kwargs
                            )

        self.tail = tail_len
        self.head = head_len
        self.width = width_len
        self._fill_form = fill_form
        self.lines_width = lines_width

        self._points = None
        self._scale_per_second = scale_per_second
        self.tail_scale_per_second = self.tail * scale_per_second[0]
        self.head_scale_per_second = self.head * scale_per_second[1]
        self.width_scale_per_second = self.width * scale_per_second[2]

        self._live_time = live_time

        self.build_points()

    def scale(self, dt):
        self.tail -= self.tail_scale_per_second * dt
        self.head -= self.head_scale_per_second * dt
        if self.width > 0:
            self.width -= self.width_scale_per_second * dt

    def update(self):
        if self._alive:
            self._clock_dt = delta_time = self._clock.d_time
            self.update_color()
            self.change_angle(delta_time)

            self.make_step()

            self.use_stop_force()

            if self.out_of_arena():
                self.stop()

            self._alive = self.alive_condition(self)
            self.scale(dt=delta_time)

            if self._speed or self._angle_change or any(self._scale_per_second):
                self.build_points()

            if self._live_time is not None:
                self._live_time -= self._clock_dt
                self._alive = self._live_time > 0

            if self.dead:
                self.start_dead_effect()

    def build_points(self):
        dx, dy = self._camera.camera
        xp, yp = self.position

        points = []
        for (angle, length) in ((0.0000001, self.tail), (1.5707963267948966, self.width),  # 0, 90
                                (3.141592653589793, self.head), (4.71238898038469, self.width)):  # 180, 270
            x = cos(angle + self._angle) * length
            y = sin(angle + self._angle) * length
            points.append((xp + dx + x, yp + dy + y))
        self._points = points

    def draw(self):
        if self._fill_form:
            self.DRAW_POLYGON(self._screen, normalize_color(self._color.copy()), self._points)
        else:
            self.DRAW_LINES(self._screen, normalize_color(self._color.copy()), 1, self._points, 3)

        # dx, dy = self._camera.camera
        # x, y = self.position

        # if self.width > 1 and self.tail > 1 and self.head > 1:
        #     surf = Surface((int(self.head + self.tail), int(self.width + self.width)))
        #
        #     draw_polygon(surf, normalize_color((100, 100, 255)), ((self.head, self.width + self.width),
        #                                                           (0, self.width),
        #                                                           (self.head, 0),
        #                                                           (self.head + self.tail, self.width),
        #                                                           )
        #                  )
        #
        #     surf = transform.rotate(surf, -degrees(self._angle))
        #     surf.set_colorkey((0, 0, 0))
        #
        #     self._screen.blit(surf, (x + dx - surf.get_width() // 2, y + dy - surf.get_height() // 2),
        #                       special_flags=BLEND_RGB_ADD)

        # end_pos = (int(self.position[0] + 50 * self._angle_k[0]), int(self.position[1] + 50 * self._angle_k[1]))
        # line(self.screen, (0, 255, 255), self.int_position, end_pos, 3)
        # circle(self.screen, (0, 0, 255), self.int_position, 3)

    @staticmethod
    def alive_condition(self):
        return self.width > 0 and self.tail >= 0 and self.head > 0 and self._speed > 0

    def out_of_arena(self):
        return not any(map(self.arena.collide_point, self._points))
