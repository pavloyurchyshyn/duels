from obj_properties.circle_form import Circle
from common_things.common_functions import get_angle_between_dots
from math import radians


class HalfCircle(Circle):
    def __init__(self, x, y, R, angle=90, hitbox_angle=180):
        super().__init__(x=x, y=y, R=R)

        self._hitbox_angle = radians(hitbox_angle) / 2
        self._angle = radians(angle)

    def collide_circle(self, xy: tuple, R) -> bool:
        if get_angle_between_dots(self._center, xy):
            return super().collide_circle(xy, R)
