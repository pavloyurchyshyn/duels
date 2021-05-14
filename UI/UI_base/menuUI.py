from common_things.global_clock import GLOBAL_CLOCK
from abc import abstractmethod
from pygame import Surface, SRCALPHA

from obj_properties.rect_form import Rectangle
from settings.window_settings import SCREEN_W, SCREEN_H, MAIN_SCREEN

from UI.UI_base.buttonUI import Button
from common_things.global_mouse import GLOBAL_MOUSE


class MenuUI(Rectangle):
    CLICK_DELAY = 0.5  # -------------->||
    SCREEN_W = SCREEN_W
    SCREEN_H = SCREEN_H

    GLOBAL_MOUSE = GLOBAL_MOUSE

    def __init__(self,
                 buttons: dict = {},

                 screen=None,

                 background_color=(0, 0, 0, 120),  # r, g, b, t
                 transparent=None,

                 size_x=SCREEN_W,
                 size_y=SCREEN_H,
                 x=0, y=0,

                 picture=None,
                 x_pic=0,
                 y_pic=0

                 ):

        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)

        # --------- BACKGROUND ------------------
        self._background_t = transparent
        self._background_color = background_color
        # ---------------------------------------

        self._clock = GLOBAL_CLOCK
        self.next_click = GLOBAL_CLOCK.time

        self._screen = screen if screen else MAIN_SCREEN

        self._buttons_values = buttons
        self._buttons = []

        self._elements = []

        self._surface = self.get_surface()

        self._picture = picture
        self._x_pic = x_pic
        self._y_pic = y_pic

    @abstractmethod
    def _update(self):
        raise NotImplementedError

    @abstractmethod
    def draw(self, dx=0, dy=0):
        self._draw(dx, dy)

    def _draw(self, dx=0, dy=0):
        # if self._background_color:
        #     flags = 0
        #     if self._background_t:
        #         flags = SRCALPHA
        #
        #     self._surface.fill(self._background_color, special_flags=flags)

        self._screen.blit(self._surface, (self._x_pic + dx, self._y_pic + dy))
        if self._picture:
            self._screen.blit(self._picture, (self.x0 + dx, self.y0 + dy))

        for element in self._elements:
            element.draw(dx, dy)

    def create_buttons(self):
        for button in self._buttons_values:
            b = Button(*self._buttons_values[button]['args'], **self._buttons_values[button]['kwargs'],
                       screen=self._surface)
            self._elements.append(b)
            self._buttons.append(b)
            setattr(self, button, b)

        self._elements.sort(key=self.__sort_value, reverse=True)
        self._buttons.sort(key=self.__sort_value, reverse=True)

    def create_button_from_data(self, buttons_data: dict, surface=None):
        buttons = []
        surface = surface if surface else self._surface
        for button in buttons_data:
            b = Button(*buttons_data[button]['args'], **buttons_data[button]['kwargs'],
                       screen=surface)
            buttons.append(b)
            setattr(self, button, b)

        buttons.sort(key=self.__sort_value, reverse=True)

        return buttons

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
    def surface(self):
        return self._surface

    @staticmethod
    def __sort_value(element):
        """
        For sort.

        :param element: Rectangle or Circle object
        :return:
        """
        return element.y0
