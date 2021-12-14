from math import cos, sin, dist, radians, sqrt
from common_things.common_functions import get_angle_between_dots
from interfaces.collide_interfaces import CollideInterface
from obj_properties.properties_constants import CIRCLE_TYPE, RECT_TYPE, SEMI_CIRCLE_TYPE, LINE_TYPE


class Line(CollideInterface):
    FORM_TYPE = LINE_TYPE

    def __init__(self, xy0, xy1: list = None, angle=None, length=None):
        self._dots = []
        self.build(xy0, xy1, angle, length)

        self._collide_able = 1

    @property
    def first_dot(self):
        return self.x0, self.y0

    @property
    def second_dot(self):
        return self.x1, self.y1

    def _make_dots(self):
        self._dots.clear()
        self._dots.append((self.x0, self.y0))
        self._dots.append((self.x1, self.y1))

    def check_for_dots_replacing(self):
        if self.x0 > self.x1:
            self.x0, self.x1 = self.x1, self.x0
            self.y0, self.y1 = self.y1, self.y0
            # (self.x0, self.y0), (self.x1, self.y1) = (self.x1, self.y1), (self.x0, self.y0)

    def build(self, xy: list, xy1=None, angle=None, length=None):
        if xy1 == angle == length == None:
            raise Exception('Bad arguments!')

        self.x0, self.y0 = xy

        if xy1:
            self.x1, self.y1 = xy1
            # self.check_for_dots_replacing()
            self._make_dots()
            self._length = dist(*self._dots)
            self._angle = round(get_angle_between_dots(*self._dots), 2)
        else:
            self._angle = round(angle, 2)
            self._length = length
            self.x1 = self.x0 + cos(angle) * length
            self.y1 = self.y0 + sin(angle) * length
            # self.check_for_dots_replacing()
            self._make_dots()

    def _change_position(self, xy: list = None, xy1=None, angle=None, length=None, make_dots=None) -> None:
        xy = xy if xy else (self.x0, self.y0)

        if xy1 == angle == length == None:
            x1 = xy[0] + cos(self._angle) * self.length
            y1 = xy[1] + sin(self._angle) * self.length
            xy1 = x1, y1

        elif length and (angle is None):
            angle = self._angle

        elif angle and (length is None):
            length = self._length

        self.build(xy, xy1, angle, length)

    @property
    def length(self):
        return self._length

    @property
    def dots(self):
        return self._dots

    def collide_line(self, line_obj) -> bool:
        return self._collide_line(line_f_dot=line_obj.first_dot,
                                  line_s_dot=line_obj.second_dot,
                                  angle=line_obj._angle,
                                  )

    def collide_rect(self, rect_obj):
        for dot in self._dots:
            if rect_obj.collide_point(dot):
                return True

        f_dot = rect_obj._dots[-1]
        for dot in rect_obj._dots:
            if self._collide_line(line_f_dot=f_dot, line_s_dot=dot, angle=get_angle_between_dots(f_dot, dot)):
                return 1
            f_dot = dot

        return 0

    def _collide_line(self, line_f_dot, line_s_dot, angle):
        if self._angle == angle:
            for dot in (line_f_dot, line_s_dot):
                if self.collide_point(dot):
                    return True

            return False

        else:
            ax1, ay1 = self.first_dot
            ax2, ay2 = self.second_dot
            bx1, by1 = line_f_dot
            bx2, by2 = line_s_dot

            # ax1, ay1, ax2, ay2 = (ax2, ay2, ax1, ay1) if ax1 >= ax2 else (ax1, ay1, ax2, ay2)
            # bx1, by1, bx2, by2 = (bx2, by2, bx1, by1) if bx1 >= bx2 else (bx1, by1, bx2, by2)

            v1 = (bx2 - bx1) * (ay1 - by1) - (by2 - by1) * (ax1 - bx1)
            v2 = (bx2 - bx1) * (ay2 - by1) - (by2 - by1) * (ax2 - bx1)
            v3 = (ax2 - ax1) * (by1 - ay1) - (ay2 - ay1) * (bx1 - ax1)
            v4 = (ax2 - ax1) * (by2 - ay1) - (ay2 - ay1) * (bx2 - ax1)

            return (v1 * v2 < 0) and (v3 * v4 < 0)

    def collide_point(self, xy: list) -> bool:
        # (x - x0) * (y1 - y0) - (x1 - x0) * (y - y0) = 0
        return (xy[0] - self.x0) * (self.y1 - self.y0) - (self.x1 - self.x0) * (xy[1] - self.y0) == 0

    def collide_circle(self, xy: list, R) -> bool:
        x1, y1 = self.x0, self.y0
        x2, y2 = self.x1, self.y1
        x3, y3 = xy

        a = (x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1)
        b = 2 * ((x2 - x1) * (x1 - x3) + (y2 - y1) * (y1 - y3))
        c = x3 * x3 + y3 * y3 + x1 * x1 + y1 * y1 - 2 * (x3 * x1 + y3 * y1) - R * R

        if -b < 0:
            return c < 0
        if -b < (2.0 * a):
            return 4.0 * a * c - b * b < 0

        return a + b + c < 0

    def collide_dots(self, other) -> bool:
        for dot in other._dots:
            if self.collide_point(dot):
                return 1
        return 0

    def collide(self, other) -> bool:
        if self._collide_able:
            if other.FORM_TYPE == self.FORM_TYPE:
                return self.collide_line(other)

            elif other.FORM_TYPE == RECT_TYPE:
                return self.collide_rect(rect_obj=other)

            elif other.FORM_TYPE == CIRCLE_TYPE:
                return self.collide_circle(other._center, other._size)

            return self.collide_dots(other)
        else:
            return False

    def scale(self, k):
        raise NotImplementedError

    @property
    def position(self):
        return self.x0, self.y0
    # def get_center(self):
