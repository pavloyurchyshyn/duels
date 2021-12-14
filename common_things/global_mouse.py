from settings.window_settings import MAIN_SCREEN
# from settings.screen_size import GAME_SCALE
from settings.default_common_settings import DEFAULT_CROSSHAIR_SIZE
from common_things.save_and_load_json_config import get_param_from_cgs, save_param_to_cgs
from common_things.sprites_functions import get_surface
from settings.default_common_settings import CROSSHAIR_SURFACE_SIZE_KEY, DEFAULT_CROSSHAIR_SIZE, \
    DEFAULT_CROSSHAIR_DOT_EXISTS, DEFAULT_CROSSHAIR_DOT_SIZE, DEFAULT_CROSSHAIR_LINE_SIZE, \
    CROSSHAIR_DOT_EXISTS_KEY, CROSSHAIR_DOT_SIZE_KEY, CROSSHAIR_LINE_SIZE_KEY, \
    DEFAULT_CROSSHAIR_LINE_CENTER_DISTANCE, CROSSHAIR_LINE_CENTER_DISTANCE_KEY, \
    DEFAULT_CROSSHAIR_LINE_WIGHT, CROSSHAIR_LINE_WIGHT_KEY, \
    DEFAULT_CROSSHAIR_ROTATE, CROSSHAIR_ROTATE_KEY, DEFAULT_CROSSHAIR_COLOR, CROSSHAIR_COLOR_KEY
from pygame.draw import line as draw_line
from pygame.draw import circle as draw_circle
from pygame import mouse
from pygame.transform import rotate

from math import cos, sin, radians


class Mouse:
    MOUSE_SIZE = (DEFAULT_CROSSHAIR_SIZE, DEFAULT_CROSSHAIR_SIZE)#(DEFAULT_CROSSHAIR_SIZE * GAME_SCALE, DEFAULT_CROSSHAIR_SIZE * GAME_SCALE)
    MAIN_SCREEN = MAIN_SCREEN

    def __init__(self, rel=None, pos=None, pressed=None):
        self.mouse = mouse
        self._rel = self.mouse.get_rel() if rel is None else rel
        self._pos = self.mouse.get_pos() if pos is None else pos
        self._pressed = self.mouse.get_pressed() if pressed is None else pressed
        self._scroll_top = 0
        self._scroll_bot = 0

        self._size = get_param_from_cgs(CROSSHAIR_SURFACE_SIZE_KEY)
        self._line_size = DEFAULT_CROSSHAIR_LINE_SIZE
        self._dot_exists = DEFAULT_CROSSHAIR_DOT_EXISTS
        self._dot_size = DEFAULT_CROSSHAIR_DOT_SIZE
        self._line_center_distance = DEFAULT_CROSSHAIR_LINE_CENTER_DISTANCE
        self._line_wight = DEFAULT_CROSSHAIR_LINE_WIGHT
        self._rotate = DEFAULT_CROSSHAIR_ROTATE
        self._color = DEFAULT_CROSSHAIR_COLOR

        self._picture = None

        self.load_crosshair_parameters()
        self.create_crosshair()
        # try:
        #     from common_things.img_loader import load_image
        #     self._picture = load_image('sprites/m_cursor.png', Mouse.MOUSE_SIZE, 0, smooth_scale=False)
        #     mouse.set_pos(500, 500)
        # except:
        #     pass

        self.mouse.set_visible(False)

    def update(self):
        self._rel = self.mouse.get_rel()
        self._pos = [*self.mouse.get_pos()]
        self._pressed = self.mouse.get_pressed()
        self._scroll_top = 0
        self._scroll_bot = 0

    def set_position(self, pos):
        self.mouse.set_pos(pos)

    def load_crosshair_parameters(self):
        data = (('_size', CROSSHAIR_SURFACE_SIZE_KEY, DEFAULT_CROSSHAIR_SIZE),
                ('_line_size', CROSSHAIR_LINE_SIZE_KEY, DEFAULT_CROSSHAIR_LINE_SIZE),
                ('_dot_exists', CROSSHAIR_DOT_EXISTS_KEY, DEFAULT_CROSSHAIR_DOT_EXISTS),
                ('_dot_size', CROSSHAIR_DOT_SIZE_KEY, DEFAULT_CROSSHAIR_DOT_SIZE),
                ('_line_center_distance', CROSSHAIR_LINE_CENTER_DISTANCE_KEY, DEFAULT_CROSSHAIR_LINE_CENTER_DISTANCE),
                ('_line_wight', CROSSHAIR_LINE_WIGHT_KEY, DEFAULT_CROSSHAIR_LINE_WIGHT),
                ('_rotate', CROSSHAIR_ROTATE_KEY, DEFAULT_CROSSHAIR_ROTATE),
                ('_color', CROSSHAIR_COLOR_KEY, DEFAULT_CROSSHAIR_COLOR),
                )

        for self_parametr, key, default_value in data:
            new_value = get_param_from_cgs(key)
            if new_value:
                setattr(self, self_parametr, new_value)
            else:
                setattr(self, self_parametr, default_value)
                save_param_to_cgs(key, default_value)

    def create_crosshair(self):
        crosshair_surface = get_surface(size_x=self._size, transparent=1)
        surface_center = (self._size // 2, self._size // 2)

        for angle in (0, 90, 180, 270):
            angle = radians(angle)

            start_line_position = (surface_center[0] + cos(angle) * self._line_center_distance,
                                   surface_center[1] + sin(angle) * self._line_center_distance)

            end_line_position = (start_line_position[0] + cos(angle) * self._line_size,
                                 start_line_position[1] + sin(angle) * self._line_size)

            draw_line(crosshair_surface, self._color, start_line_position, end_line_position, self._line_wight)

        if self._dot_exists:
            draw_circle(crosshair_surface, self._color, surface_center, self._dot_size)

        self._picture = rotate(crosshair_surface, self._rotate)

    def draw(self):
        Mouse.MAIN_SCREEN.blit(self._picture, (self._pos[0] - self._picture.get_width() // 2,
                                               self._pos[1] - self._picture.get_height() // 2))

    @property
    def lmb(self):
        return self._pressed[0]

    @property
    def network_data(self):
        return self._pressed, self._pos

    @property
    def data(self):
        return self._pressed, self._scroll_top, self._scroll_bot, self._pos, self._rel

    @property
    def scroll_top(self):
        return self._scroll_top

    @scroll_top.setter
    def scroll_top(self, value):
        self._scroll_top = value

    @property
    def scroll_bot(self):
        return self._scroll_bot

    @scroll_bot.setter
    def scroll_bot(self, value):
        self._scroll_bot = value

    @property
    def scroll(self):
        return self._scroll_top, self._scroll_bot

    @property
    def rel(self):
        return self._rel

    @property
    def pos(self):
        return self._pos

    @property
    def pressed(self):
        return self._pressed


GLOBAL_MOUSE = Mouse()
