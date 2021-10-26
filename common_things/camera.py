from settings.screen_size import SCREEN_H, SCREEN_W, HALF_SCREEN_W, HALF_SCREEN_H#, X_SCALE, Y_SCALE, GAME_SCALE
from settings.arena_settings import STANDARD_ARENA_SIZE


class Camera:
    def __init__(self, x: int, y: int):
        self.camera_x = x
        self.camera_y = y
        self.max_x = SCREEN_W - int(STANDARD_ARENA_SIZE) + 2
        self.max_y = SCREEN_H - int(STANDARD_ARENA_SIZE) + 2

#        self.max_x = SCREEN_W - int(STANDARD_ARENA_SIZE * GAME_SCALE) + 2
#        self.max_y = SCREEN_H - int(STANDARD_ARENA_SIZE * GAME_SCALE) + 2

        self.min_x = 0
        self.min_y = 0

        self.dx = self.dy = 0
        self.old_dx = x
        self.old_dy = y

        self.default_camera = [HALF_SCREEN_W - x, HALF_SCREEN_H - y]
        self.current_default_camera = self.default_camera
        self._camera = [HALF_SCREEN_W - x, HALF_SCREEN_H - y]

    def reload(self, x: int, y: int):  # , max_x: int, max_y: int):
        self.__init__(x, y)  # , max_x, max_y)

    def set_dx_dy(self, dx, dy):
        self._camera = [dx, dy]

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

        self._camera = ([int(self.default_camera[0] + self.dx), int(self.default_camera[1] + self.dy)])

        self.__normalize_camera()

        self.old_dx, self.old_dy = player_pos


GLOBAL_CAMERA = Camera(0, 0)
