from settings.screen_size import SCREEN_H, SCREEN_W, HALF_SCREEN_W, HALF_SCREEN_H
from settings.arena_settings import STANDARD_ARENA_X_SIZE, STANDARD_ARENA_Y_SIZE
from common_things.global_clock import GLOBAL_CLOCK, ROUND_CLOCK
from math import sin, cos, dist


class Camera:
    def __init__(self, x: int, y: int, round_clock: bool = 1, player=None):
        self.camera_x = x
        self.camera_y = y
        self._player = player
        self.max_x = SCREEN_W - int(STANDARD_ARENA_X_SIZE) + 2
        self.max_y = SCREEN_H - int(STANDARD_ARENA_Y_SIZE)

        self._old_player_pos = [-9999, -9999]
        self._old_player_angle = None

        self._move_speed = 1000
        self._max_range = 100
        self._angle_add = 250

        self.min_x = 0
        self.min_y = 0

        self.dx = self.dy = 0
        self.old_dx = x
        self.old_dy = y

        self.default_camera = [HALF_SCREEN_W - x, HALF_SCREEN_H - y]
        self.current_default_camera = self.default_camera

        self._camera = [HALF_SCREEN_W - x, HALF_SCREEN_H - y]
        self._clock = None
        if self._clock:
            self._move_speed *= self._clock.d_time
        self.set_clock(round_clock=round_clock)
        self._real_position = [0, 0]
        self.update()

    def unfollow_player(self):
        self._player = None
        self._camera = [0, 0]
        self._real_position = [0, 0]

    def follow_player(self, player):
        self._old_player_pos = [-9999, -9999]
        self._player = player
        self.update()

    def set_clock(self, round_clock=1):
        self._clock = ROUND_CLOCK if round_clock else GLOBAL_CLOCK

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

    def move_camera(self):
        if self._camera != self._real_position:
            for i in range(2):
                real_pos = self._real_position[i]
                current_pos = self._camera[i]
                if current_pos < real_pos:
                    current_pos += self._move_speed
                    if current_pos >= real_pos:
                        current_pos = real_pos

                elif current_pos > real_pos:
                    current_pos -= self._move_speed * self._clock.d_time

                    if current_pos <= real_pos:
                        current_pos = real_pos

                self._camera[i] = current_pos

        self.__normalize_camera()

    def update(self):
        if self._player and self._player.alive:
            player_pos = self._player.position
            player_angle = self._player.angle

            if player_pos != self._old_player_pos:
                self._real_position = [int(self.default_camera[0] + self.dx), int(self.default_camera[1] + self.dy)]

                self.dx += self.old_dx - player_pos[0]
                self.dy += self.old_dy - player_pos[1]

                self.old_dx, self.old_dy = player_pos
                self._old_player_pos = player_pos

            # if player_angle is not None:
            #     self._real_position = [int(self.default_camera[0] + self.dx), int(self.default_camera[1] + self.dy)]
            #
            #     self._real_position[0] = self._real_position[0] - cos(player_angle) * self._angle_add
            #     self._real_position[1] = self._real_position[1] - sin(player_angle) * self._angle_add

        self.move_camera()


GLOBAL_CAMERA = Camera(0, 0)
