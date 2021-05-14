from settings.window_settings import SCREEN_H, SCREEN_W, HALF_SCREEN_W, HALF_SCREEN_H
from settings.arena_settings import ELEMENT_SIZE, STANDARD_ARENA_CELL_SIZE


class Camera:
    def __init__(self, x: int, y: int):  # , max_x: int, max_y: int):
        self.camera_x = x
        self.camera_y = y
        self.max_x = SCREEN_W - STANDARD_ARENA_CELL_SIZE #- ELEMENT_SIZE // 2
        self.max_y = SCREEN_H - STANDARD_ARENA_CELL_SIZE #- ELEMENT_SIZE // 2
        self.min_x = 0
        self.min_y = 0  # + WALL_CELL_SIZE // 2

        self.dx = self.dy = 0
        self.old_dx = x
        self.old_dy = y

        self.default_camera = [HALF_SCREEN_W - x, HALF_SCREEN_H - y]
        self._camera = [HALF_SCREEN_W - x, HALF_SCREEN_H - y]

    def reload(self, x: int, y: int):  # , max_x: int, max_y: int):
        self.__init__(x, y)  # , max_x, max_y)

    def __normalize_camera(self):
        if self._camera[0] > self.min_x:
            self._camera[0] = self.min_x
        elif self._camera[0] < self.max_x:
            self._camera[0] = self.max_x

        if self._camera[1] > self.min_y:
            self._camera[1] = self.min_y
        elif self._camera[1] < self.max_y:
            self._camera[1] = self.max_y

    @property
    def camera(self):
        return self._camera

    def update(self, player_pos):
        self.dx += self.old_dx - player_pos[0]
        self.dy += self.old_dy - player_pos[1]

        self._camera = [self.default_camera[0] + self.dx, self.default_camera[1] + self.dy]

        self.__normalize_camera()

        self.old_dx, self.old_dy = player_pos


GLOBAL_CAMERA = Camera(0, 0)
