from math import sin, cos, radians, dist
from interfaces.collide_interfaces import CollideInterface
from abc import abstractmethod
from obj_properties.properties_constants import CIRCLE_TYPE, RECT_TYPE, SEMI_CIRCLE_TYPE, LINE_TYPE, POINT_TYPE


class Circle(CollideInterface):
    """
    Circle object.
    """
    FORM_TYPE = CIRCLE_TYPE

    def __init__(self, x: int, y: int, R: int, dots_angle: bool or int = False, angle=0) -> None:
        self._original_size: float = R  # radius
        self._size: float = R  # radius
        self.h_size = R / 2
        self._center: list = [x, y]
        self._dots: list = []
        self._make_dots = self.__make_dots_with_angle if dots_angle else self.__make_dots
        self._angle = angle
        self._collide_able = 1
        self._make_dots()

    def _change_position(self, xy: list, make_dots=0, angle=None) -> None:
        """
        Changing position of object center.

        :param xy: tuple(int, int)
        :return:
        """
        if angle:
            self._angle = angle

        if self._center != xy:
            self._center = xy

        if make_dots:
            self._make_dots()

    @abstractmethod
    def make_original_size(self):
        self._make_original_size()

    def _make_original_size(self):
        self._size = self._original_size
        self._change_position(self._center)

    @abstractmethod
    def scale(self, k):
        self._scale(k)

    def _scale(self, k):
        new_size = k * self._size
        if new_size >= 1:
            self._size = new_size
            self._change_position(self._center)

    def __make_dots(self) -> None:
        """
        Rebuilding dots position.

        :return:
        """
        self._dots.clear()
        x, y = self._center
        self._dots.append(self._center)
        if self._size >= 1:
            size = self._size

            for angle in range(0, 360, 30):
                x1: int = int(x + cos(radians(angle)) * size)
                y1: int = int(y + sin(radians(angle)) * size)
                self._dots.append((x1, y1))

    def collide_circle(self, xy: tuple, R) -> bool:
        """
        Returns True if circle on xy position with radius R collide object.

        :param xy: position of other object
        :param R: radius of other object
        :return:
        """

        return dist(xy, self._center) <= self._size + R

    def collide_dots(self, other) -> bool:
        """
        If at least one dot of object inside returns True.

        :param other: Circle or Rectangle object
        :return:
        """
        for dot in other._dots:
            if self.collide_point(dot):
                return True

        return False

    def collide_point(self, xy: list) -> bool:
        """
        Returns True if dot inside circle, if range between center and dot <= radius

        :param xy: position of dot
        :return:
        """

        return dist(xy, self._center) <= self._size

    def collide(self, other) -> bool:
        """
        Returns True if collide object

        :param other:
        :return: bool
        """

        if self._collide_able:
            if other.FORM_TYPE == self.FORM_TYPE:
                return self.collide_circle(other._center, other._size)

            elif other.FORM_TYPE == RECT_TYPE:
                return other.collide_circle(self._center, self._size)

            elif other.FORM_TYPE == LINE_TYPE:
                return other.collide_circle(self._center, self._size)

            elif other.FORM_TYPE == POINT_TYPE:
                return self.collide_point(other._center)

            return self.collide_dots(other)
        else:
            return 0

    def get_size(self):
        return self._size

    def get_pos(self):
        return self._center

    def __make_dots_with_angle(self, a=None):
        a = self._angle if a is None else a
        self._dots.clear()
        x, y = self._center
        self._dots.append(self._center)

        size = self._size

        for angle in range(0, 360, 30):
            x1: int = int(x + cos(radians(angle) + a) * size)
            y1: int = int(y + sin(radians(angle) + a) * size)
            self._dots.append((x1, y1))

    @property
    def dots(self):
        if self._collide_able:
            return self._dots

        return ()
