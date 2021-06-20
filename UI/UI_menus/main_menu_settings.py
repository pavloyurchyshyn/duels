from UI.UI_base.menu_UI import MenuUI

from common_things.global_mouse import GLOBAL_MOUSE
from common_things.global_keyboard import GLOBAL_KEYBOARD

from settings.UI_setings.menus_settings.main_menu_settings import MAIN_MENU_SETTINGS_BUTTONS, back_to_menu, \
    MUSIC_VOLUME_VALUE, VOLUME_PROGRESS_BAR, MUTE_MUSIC


class MainMenuSettings(MenuUI):
    def __init__(self):
        super().__init__(buttons=MAIN_MENU_SETTINGS_BUTTONS)
        self.create_buttons()
        self._stage = None
        self._chosen_button = None
        self._mus_value = MUSIC_VOLUME_VALUE

    def update(self):
        for button in self._buttons:
            button.update()

        if GLOBAL_KEYBOARD.ESC:
            back_to_menu()

        if GLOBAL_MOUSE.lmb:
            xy = self.GLOBAL_MOUSE.pos
            for button in self._buttons:
                button.click(xy=xy)
                if button.clicked:
                    break

            MUTE_MUSIC.click(xy=xy)

    def draw(self, dx=0, dy=0):
        self._draw(dx, dy)
        self._mus_value.draw(dx, dy)
        VOLUME_PROGRESS_BAR.draw(dx, dy)
        MUTE_MUSIC.draw(dx, dy)

    def _update(self):
        pass


MAIN_MENU_SETTINGS_UI = MainMenuSettings()
