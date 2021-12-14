from math import radians, cos, sin, dist
from interfaces.collide_interfaces import CollideInterface
from common_things.common_functions import get_angle_between_dots
from obj_properties.properties_constants import CIRCLE_TYPE, RECT_TYPE, SEMI_CIRCLE_TYPE, LINE_TYPE


class SemiCircle(CollideInterface):
    ANGLES = [radians(angle) for angle in range(-91, 90, 10)]
    FORM_TYPE = SEMI_CIRCLE_TYPE

    def __init__(self, x, y, angle,
                 angles=None,
                 R=50):
        self._center = [x, y]
        self._r = R
        self._dots = []
        self._angle = angle
        self._angles = angles if angles else self.ANGLES
        self._min_a = min(self._angles)
        self._max_a = max(self._angles)

    def change_angle(self, angle, build_dots=1):
        self._angle = angle
        if build_dots:
            self.__make_dots()

    def _change_position(self, xy: list) -> None:
        self._center = xy
        self.__make_dots()

    def __make_dots(self):
        self._dots.clear()
        x0, y0 = self._center
        for angle in self._angles:
            x = x0 + cos(angle + self._angle) * self._r
            y = y0 + sin(angle + self._angle) * self._r

            self._dots.append((x, y))

    def collide_circle(self, xy: list, R) -> bool:
        dist_to_dot = dist(xy, self._center)
        if dist_to_dot <= R:
            return True

        else:
            return self.collide_point(xy)

    def collide_dots(self, other) -> bool:
        for dot in other._dots:
            if self.collide_point(dot):
                return True
        return False

    def collide_point(self, xy: list) -> bool:
        a = get_angle_between_dots(self._center, xy)
        return dist(xy, self._center) <= self._r and self._min_a + self._angle <= a <= self._max_a + self._angle

    def collide(self, other) -> bool:
        return self.collide_dots(other)
