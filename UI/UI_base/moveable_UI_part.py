from common_things.global_mouse import GLOBAL_MOUSE
from common_things.global_clock import GLOBAL_CLOCK

from obj_properties.rect_form import Rectangle
from settings.UI_setings.button_settings import DEFAULT_BUTTON_X_SIZE1, \
    DEFAULT_BUTTON_Y_SIZE1, DEFAULT_CLICK_DELAY
from settings.global_parameters import GLOBAL_SETTINGS

from pygame import Surface, SRCALPHA, draw

from UI.UI_base.text_UI import Text


class MoveableUI(Rectangle):
    BUTTON_X_SIZE = DEFAULT_BUTTON_X_SIZE1
    BUTTON_Y_SIZE = DEFAULT_BUTTON_Y_SIZE1
    MOUSE = GLOBAL_MOUSE
    CLOCK = GLOBAL_CLOCK
    MOVE_TIME = 0.15

    GLOBAL_SETTINGS = GLOBAL_SETTINGS

    def __init__(self, x, y,
                 screen,
                 size_x=None, size_y=None,
                 text: str = '',
                 background_color=(0, 0, 0, 120),  # r, g, b, t
                 transparent=None,
                 value=None,
                 UI_elements=[],
                 hideable=0
                 ):
        size_x = size_x if size_x else MoveableUI.BUTTON_X_SIZE
        size_y = size_y if size_y else MoveableUI.BUTTON_Y_SIZE

        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)

        self._screen = screen

        self._background_color = background_color  # r, g, b, t
        self._background_t = transparent
        self._background_surf = self.get_surface()

        self._elements = UI_elements
        self._value = value

        self._text = text
        self._text_r = None

        self.build_text()
        self.build()

        self._move = None
        self._hideable = hideable

    def update(self):
        self._update()

    def _update(self):
        if self._move:
            dx, dy = MoveableUI.MOUSE.rel
            self.change_position_lt((self.x0 + dx, self.y0 + dy))
            self.build()
            if self._move < MoveableUI.CLOCK.time:
                self._move = None

    def click(self, xy, *args, **kwargs):
        if self.collide_point(xy):
            self._move = MoveableUI.CLOCK.time + MoveableUI.MOVE_TIME
            return

        else:
            for element in self._elements:
                res = element.click(xy, *args, *kwargs)
                if res:
                    return res

    def build_text(self):
        if self._text:
            self._text_r = Text(text=self._text, screen=self._background_surf)

    def build(self):

        dy = 0
        for UI_element in self._elements:
            UI_element.change_position_lt((self.x0, self.y1 + dy))
            dy += UI_element.height

    def draw(self, dx=0, dy=0):
        if MoveableUI.GLOBAL_SETTINGS['test_draw']:
            for dot in self._dots:
                draw.circle(self._screen, (255, 255, 255), dot, 2)
        self._draw(dx, dy)

    def _draw(self, dx=0, dy=0):
        if self._background_surf:
            self._screen.blit(self._background_surf, (self.x0 + dx, self.y0 + dy))

        for element in self._elements:
            element.draw(dx, dy)

    def get_surface(self):
        flags = 0
        if self._background_t:
            flags = SRCALPHA

        surface = Surface((self.size_x, self.size_y), flags, 32)
        if self._background_color:
            surface.fill(self._background_color)

        surface.convert_alpha()

        return surface

    @property
    def value(self):
        return self._value
