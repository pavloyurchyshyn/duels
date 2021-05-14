from UI.UI_base.menuUI import MenuUI

from common_things.global_mouse import GLOBAL_MOUSE
from common_things.global_keyboard import GLOBAL_KEYBOARD

from settings.UI_setings.menus_settings.main_menu_settings import MAIN_MENU_SETTINGS_BUTTONS

from pygame import Rect


class MainMenuSettings(MenuUI):
    def __init__(self):
        super().__init__(buttons=MAIN_MENU_SETTINGS_BUTTONS)
        self.create_buttons()
        self._stage = None
        self._chosen_button = None

    def update(self):
        for button in self._buttons:
            button.update()

        if GLOBAL_MOUSE.lmb:
            for button in self._buttons:
                button.click(xy=self.GLOBAL_MOUSE.pos)
                if button.clicked:
                    break

    def draw(self, dx=0, dy=0):
        self._draw(dx, dy)

    def _update(self):
        pass


MAIN_MENU_SETTINGS_UI = MainMenuSettings()