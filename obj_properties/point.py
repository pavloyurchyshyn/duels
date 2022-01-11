from interfaces.collide_interfaces import CollideInterface
from obj_properties.properties_constants import CIRCLE_TYPE, RECT_TYPE, SEMI_CIRCLE_TYPE, LINE_TYPE, POINT_TYPE
from math import dist


class Point(CollideInterface):
    FORM_TYPE = POINT_TYPE

    def collide_point(self, xy: list) -> bool:
        return self._center == xy

    def collide_dots(self, other) -> bool:
        for dot in other._dots:
            if self.collide_point(dot):
                return 1

        return 0

    def collide(self, other) -> bool:
        return other.collide_point(self._center)

    def collide_circle(self, xy: list, R) -> bool:
        return dist(xy, self._center) <= R

    @property
    def _dots(self):
        return (self._center,)
