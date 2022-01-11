from interfaces.collide_interfaces import CollideInterface
from abc import abstractmethod
from obj_properties.properties_constants import CIRCLE_TYPE, RECT_TYPE, SEMI_CIRCLE_TYPE, LINE_TYPE, POINT_TYPE


class Rectangle(CollideInterface):
    FORM_TYPE = RECT_TYPE

    def __init__(self, x, y, size_x, size_y=None):
        """
        Rect objects for collisions.

        :param x: x of left top corner
        :param y: y of left top corner
        :param size_x: horizontal size of box
        :param size_y: vertical size of box if not None else size_X
        """

        self.size_x = size_x
        self.original_size_x = size_x
        self.original_size_y = size_y if size_y is not None else size_x
        self.size_y = size_y if size_y is not None else size_x

        self._center = x + self.size_x // 2, y + self.size_y // 2
        self._size = self.size_x if self.size_x < self.size_y else self.size_y
        self.x0 = x
        self.x1 = x + self.size_x
        self.y0 = y
        self.y1 = y + self.size_y

        self.h_size = self._size / 2
        self._dots = []
        self._make_dots()

        self._collide_able = 1

    def get_size(self):
        return self._size

    def _make_dots(self):

        x0, y0 = self.x0, self.y0
        x1, y1 = self.x1, self.y1

        self._dots.clear()
        self._dots.append(self._center)
        self._dots.append((x0, y0))  # left top
        self._dots.append(((x0 + x1) // 2, y0))  # mid top
        self._dots.append((x1, y0))  # right top
        self._dots.append((x1, (y1 + y0) // 2))  # right mid
        self._dots.append((x1, y1))  # right bot
        self._dots.append(((x0 + x1) // 2, y1))  # mid bot
        self._dots.append((x0, y1))  # left bot
        self._dots.append((x0, (y1 + y0) // 2))  # left mid

    @abstractmethod
    def change_position(self, xy):
        self._change_position(xy)

    @abstractmethod
    def change_position_lt(self, xy: tuple):
        self._change_position_lt(xy)

    def _change_position_lt(self, xy: tuple):
        """
        New left top corner

        :param xy: int, int
        :return:
        """
        x, y = xy
        self._center = [x + self.size_x // 2, y + self.size_y // 2]
        self.x0 = x
        self.y0 = y

        self.x1 = x + self.size_x
        self.y1 = y + self.size_y
        self._make_dots()

    def _change_position(self, xy: tuple, make_dots=None):
        """
        XY -> center of object

        :param xy: int, int
        :return:
        """
        x, y = xy
        self._center = xy
        self.x0 = x - self.size_x // 2
        self.y0 = y - self.size_y // 2

        self.x1 = x + self.size_x // 2
        self.y1 = y + self.size_y // 2
        self._make_dots()

    @abstractmethod
    def scale(self, k):
        self._scale(k)

    def _scale(self, k):
        new_size_x = k * self.size_x
        new_size_y = k * self.size_y

        if new_size_x >= 1 and new_size_y >= 1:
            self.size_x = new_size_x
            self.size_y = new_size_y

            self._change_position(self._center)

    @abstractmethod
    def make_original_size(self):
        self._make_original_size()

    def _make_original_size(self):
        self.size_x = self.original_size_x
        self.size_y = self.original_size_y
        self._change_position(self._center)

    # dot inside the rectangle?
    def collide_point(self, xy: tuple) -> bool:
        x, y = xy
        return self.x0 <= x <= self.x1 and self.y0 <= y <= self.y1

    # did circle inside rectangle?
    def collide_circle(self, xy: tuple, R) -> bool:
        x, y = xy
        return self.x0 - R <= x <= self.x1 + R and self.y0 - R <= y <= self.y1 + R

    # if at least one dot inside rect
    def collide_dots(self, other) -> bool:
        for point in other._dots:
            if self.collide_point(point):
                return True

        return False

    def collide(self, other) -> bool:
        if self._collide_able:
            other_type = other.FORM_TYPE
            if other_type == self.FORM_TYPE:
                return self.collide_dots(other)

            elif other_type == CIRCLE_TYPE:
                return self.collide_circle(other._center, other.h_size)

            elif other_type == LINE_TYPE:
                return other.collide_rect(self)

            elif other_type == POINT_TYPE:
                return self.collide_point(other._center)

        return 0

    @property
    def dots(self):
        if self._collide_able:
            return self._dots

        return ()

    @property
    def left_top(self):
        return self.x0, self.y0

    @property
    def sizes(self):
        return self.size_x, self.size_y

    @property
    def center(self):
        return self._center

    def get_rect(self):
        return (self.x0, self.y0, self.size_x, self.size_y)