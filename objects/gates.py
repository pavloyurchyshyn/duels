from obj_properties.rect_form import Rectangle
from obj_properties.img_lazy_load import OnePictureLazyLoad
from common_things.camera import GLOBAL_CAMERA
from settings.objects_settings.gates_settings import *
from settings.global_parameters import test_draw_status_is_on


class BallGate(Rectangle, OnePictureLazyLoad):
    default_size = DEFAULT_GATE_SIZE

    def __init__(self, x, y, direction_right, team, size=DEFAULT_GATE_SIZE):
        """
        :param x: x of center
        :param y: y of center
        :param direction: left or right
        :param size: x_size and y_size
        """
        x_size, y_size = size
        x = x if direction_right else x - x_size
        y = y - y_size // 2
        super(BallGate, self).__init__(x, y, x_size, y_size)
        OnePictureLazyLoad.__init__(self)

        self._top_rect = Rectangle(x, y - 5, size_x=x_size, size_y=5)
        self._bot_rect = Rectangle(x, y + y_size, size_x=x_size, size_y=5)
        self.direction = direction_right
        self.team = team

    def update(self):
        pass

    def collide_borders(self, obj):
        for border in (self._top_rect, self._bot_rect):
            if border.collide(obj):
                return 1

    def draw(self):
        dx, dy = GLOBAL_CAMERA.camera
        self.DRAW_RECT(self.MAIN_SCREEN, (200, 200, 200), (self.x0 + dx, self.y0 + dy, self.size_x, self.size_y), 2)

        if test_draw_status_is_on():
            for x, y in self._dots:
                self.DRAW_CIRCLE(self.MAIN_SCREEN, (9, 255, 9), (x + dx, y + dy), 2)

            for rect in (self._top_rect, self._bot_rect):
                for x, y in rect._dots:
                    self.DRAW_CIRCLE(self.MAIN_SCREEN, (255, 0, 0), (x + dx, y + dy), 2)