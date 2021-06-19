from obj_properties.rect_form import Rectangle

from pygame import transform, Surface, mouse
from pygame.draw import rect as DrawRect
from pygame.constants import SRCALPHA
from pygame import draw

from UI.UI_base.text_UI import Text
from common_things.global_clock import GLOBAL_CLOCK
from common_things.global_mouse import GLOBAL_MOUSE

from settings.UI_setings.button_settings import DEFAULT_BUTTON_X_SIZE, \
    DEFAULT_BUTTON_Y_SIZE, DEFAULT_CLICK_DELAY
from settings.colors import simple_colors


class Scroll(Rectangle):
    BUTTON_X_SIZE = DEFAULT_BUTTON_X_SIZE
    BUTTON_Y_SIZE = DEFAULT_BUTTON_Y_SIZE
    CLICK_DELAY = DEFAULT_CLICK_DELAY
    CLOCK = GLOBAL_CLOCK
    MOUSE = GLOBAL_MOUSE
    STEP_BETWEEN_EL = 5  # pixels

    def __init__(self, x, y,
                 screen,
                 size_x=None, size_y=None,
                 static_size=1,
                 columns=1, rows=-1,
                 transparent=0, background_color=(0, 0, 0, 120),  # r, g, b, t
                 UI_elements=[],
                 h_step=None, v_step=None,
                 border=0, border_color=simple_colors['white']
                 ):
        size_x = size_x if size_x else Scroll.BUTTON_X_SIZE
        size_y = size_y if size_y else Scroll.BUTTON_Y_SIZE

        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)

        self._screen = screen
        self._h_step = h_step if h_step else Scroll.STEP_BETWEEN_EL
        self._v_step = v_step if v_step else Scroll.STEP_BETWEEN_EL

        # --------- BORDER ---------------------
        self._border = border
        self._border_color = border_color

        # --------- BACKGROUND ------------------
        self._background_t = transparent
        self._background_color = background_color

        self._main_surface = self.get_surface()
        self._surface = None

        # -----------------------------------
        self._columns = columns
        self._rows = rows
        self._static_size = static_size

        # ----------- CELLS SIZE -----------

        # -----------------------------------
        self._UI_elements = UI_elements
        self._elements_data = []
        # -----------------------------------

        self._draw_dx_dy = [0, 0]

        self.build()

    def build(self):
        self._elements_data.clear()

        self._surface = self.get_surface()

        cell_size = (self.size_x - Scroll.STEP_BETWEEN_EL * (1 + self._columns)) / self._columns
        if self._rows > -1:
            lines = self._rows
        else:
            lines = self.size_y // (cell_size + 5)

        dy = Scroll.STEP_BETWEEN_EL
        for line in range(lines):
            dx = Scroll.STEP_BETWEEN_EL
            for column in range(1, self._columns + 1):
                self._elements_data.append([Scroll.STEP_BETWEEN_EL, dy])
                dx += cell_size + Scroll.STEP_BETWEEN_EL

            dy += cell_size

        for i, element in enumerate(self._UI_elements):
            element.set_screen(self._surface)
            dx, dy = self._elements_data[i]
            element.change_position_lt(self.x0 + dx, self.y1 + dy)
            element.draw(dx, dy)

        self._surface.convert_alpha()

        rect = self._main_surface.get_rect()
        for dx, dy in self._elements_data:
            rect.x, rect.y = dx, dy
            DrawRect(self._main_surface, color=(255, 255, 255),
                     rect=rect, width=2)

        self._main_surface.convert_alpha()

    def update(self):
        ts, bs = Scroll.MOUSE.scroll

    def click(self, xy):

        xy = Scroll.MOUSE.pos

    def draw(self, dx=0, dy=0):
        self._screen.blit(self._main_surface, (dx, dy))

    def change_position_lt(self, xy: tuple):
        self._change_position_lt(xy)
        self.build()

    def add_element(self):
        pass

    def del_element(self):
        pass

    def get_surface(self):
        flags = 0
        if self._background_t:
            flags = SRCALPHA

        surface = Surface((self.size_x, self.size_y), flags, 32)
        if self._background_color:
            surface.fill(self._background_color)

        surface.convert_alpha()

        return surface
