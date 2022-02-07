from common_things.camera import GLOBAL_CAMERA
from common_things.global_clock import ROUND_CLOCK, GLOBAL_CLOCK
from common_things.global_round_parameters import GLOBAL_ROUND_PARAMETERS
from settings.window_settings import MAIN_SCREEN
from pygame.transform import rotate, scale, smoothscale
from pygame.draw import circle, line, lines, polygon, rect


class BaseEffect:
    ROUND_PARAMETERS = GLOBAL_ROUND_PARAMETERS
    EFFECT_TYPE = None

    MAIN_SCREEN = MAIN_SCREEN

    ROTATE = rotate
    SCALE = scale
    SMOOTH_SCALE = smoothscale

    DRAW_LINE = line
    DRAW_LINES = lines
    DRAW_CIRCLE = circle
    DRAW_POLYGON = polygon
    DRAW_RECT = rect

    def __init__(self, color=None, color_change=None, color_change_func=None, **kwargs):
        if self.EFFECT_TYPE is None:
            raise Exception('Bad effect type value!')

        self._picture = kwargs.get('picture')

        self._color = color
        self._color_change = color_change
        self.update_color = color_change_func if color_change_func else self.__update_color

        self._camera = kwargs.get('camera', GLOBAL_CAMERA)

        self._screen = kwargs.get('screen', self.MAIN_SCREEN)

        self._alive_time = kwargs.get('alive_time')
        if not getattr(self, '_clock', 0):
            self._clock = ROUND_CLOCK if kwargs.get('round_clock') else GLOBAL_CLOCK

    def additional_lazy_load(self):
        pass

    def __update_color(self):
        if self._color_change:
            for i in range(len(self._color)):
                self._color[i] += self._color_change[i] * self._clock.d_time

    @property
    def color(self):
        return self._color

    @property
    def screen(self):
        return self._screen
