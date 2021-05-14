from obj_properties.rect_form import Rectangle

from pygame import transform, Surface, SRCALPHA, draw
from settings.window_settings import MAIN_SCREEN, HALF_SCREEN_W, HALF_SCREEN_H, SCREEN_H
from common_things.global_clock import GLOBAL_CLOCK


class TransitionUI:
    DEFAULT_TIME = 15
    CLOCK = GLOBAL_CLOCK

    def __init__(self,
                 left_pic=None, right_pic=None,

                 screen=MAIN_SCREEN,

                 anim_time=DEFAULT_TIME,

                 background_color=(0, 0, 0, 120),  # r, g, b, t
                 transparent=None,
                 ):

        # --------- BACKGROUND ------------------
        self._background_t = transparent
        self._background_color = background_color

        self._y = 0

        self._screen = screen

        size_x, size_y = self._screen.get_size()

        self._screen_size_x = size_x

        self._size_x = size_x / 2  # half screen x size, size of one part
        self._size_y = size_y

        # ----- background surface -----------
        self._left_pic = left_pic if left_pic else self.get_surface()
        self._right_pic = right_pic if right_pic else transform.flip(self._left_pic, True, False)
        # ------------------------------------

        self._speed = self._size_x // anim_time  # moving speed
        self._anim_time = anim_time

        self._moving_time = None

        self._x_move_pos = 0

        self._move_to = 1  # to close or -1 to open

    def update(self):
        if self._moving_time is not None:
            dt = self.CLOCK.d_time

            self._moving_time += dt
            self._x_move_pos += self._speed * dt * self._move_to

            if not(0 < self._x_move_pos < self._size_x):
                self._moving_time = None
                self._move_to = 0

    def fast_open(self):
        self._x_move_pos = 0
        self._moving_time = None

    def fast_close(self):
        self._x_move_pos = self._size_x
        self._moving_time = None

    def draw(self, dx=0, dy=0):
        self._screen.blit(self._left_pic, (dx - self._size_x + self._x_move_pos, self._y + dy))
        self._screen.blit(self._right_pic, (dx + self._screen_size_x - self._x_move_pos, self._y + dy))

        draw.line(self._screen, (255, 255, 255),
                  start_pos=(self._size_x + self._x_move_pos, 0),
                  end_pos=(self._size_x + self._x_move_pos, self._size_y))

        draw.line(self._screen, (255, 255, 255),
                  start_pos=(self._screen_size_x - self._x_move_pos, 0),
                  end_pos=(self._screen_size_x - self._x_move_pos, self._size_y))

    def open(self):
        self.move(1)

    def close(self):
        self.move(-1)

    def move(self, k=0):
        if self._moving_time is not None:
            return

        if k == 0:
            k = not self._move_to

        self._moving_time = 0
        self._move_to = k

    def get_surface(self):
        flags = 0
        if self._background_t:
            flags = SRCALPHA

        surface = Surface((self._size_x, self._size_y), flags, 32)
        if self._background_color:
            surface.fill(self._background_color)

        surface.convert_alpha()

        return surface
