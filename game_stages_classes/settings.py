from UI.UI_base.menu_UI import MenuUI

from common_things.global_mouse import GLOBAL_MOUSE
from common_things.global_keyboard import GLOBAL_KEYBOARD
from common_things.stages import Stages

from settings.UI_setings.menus_settings.main_menu_settings import MAIN_MENU_SETTINGS_BUTTONS, KEYBOARD_TEXT_OBJS,\
    MUSIC_VOLUME_VALUE, VOLUME_PROGRESS_BAR, MUTE_MUSIC_BUTTON, KEYBOARD_SETTINGS_TEXT, KEYBOARD_TEXT_DATA, INPUT_ELEMENTS
from settings.game_stages_constants import MAIN_MENU_SETTINGS_STAGE
from settings.window_settings import MAIN_SCREEN
from settings.global_parameters import pause_available, pause_step

set_main_menu_stage = Stages().set_main_menu_stage


class Settings(MenuUI):
    def __init__(self):
        super().__init__(buttons=MAIN_MENU_SETTINGS_BUTTONS, name=MAIN_MENU_SETTINGS_STAGE,
                         texts=KEYBOARD_TEXT_DATA, texts_objects=KEYBOARD_TEXT_OBJS,
                         surface=MAIN_SCREEN,
                         )
        self.create_buttons()
        self.create_text()

        self._chosen_button = None
        self._music_volume_value = MUSIC_VOLUME_VALUE
        self.add_elements_to_controller(*self._buttons, *INPUT_ELEMENTS, MUTE_MUSIC_BUTTON)

    def update(self):
        for inp_el in INPUT_ELEMENTS:
            inp_el.update()

        for button in self._buttons:
            button.update()

        if GLOBAL_KEYBOARD.ESC and pause_available():
            pause_step()
            set_main_menu_stage()

        if GLOBAL_MOUSE.lmb:
            xy = self.GLOBAL_MOUSE.pos
            for button in self._buttons:
                button.click(xy=xy)
                if button.clicked:
                    break

            MUTE_MUSIC_BUTTON.click(xy=xy)

    def draw(self, dx=0, dy=0):
        self._screen.fill((0, 0, 0, 255))

        for element in self._elements:
            element.draw(dx, dy)

        self._music_volume_value.draw(dx, dy)

        KEYBOARD_SETTINGS_TEXT.draw()
        VOLUME_PROGRESS_BAR.draw(dx, dy)
        MUTE_MUSIC_BUTTON.draw(dx, dy)

        for inp_el in INPUT_ELEMENTS:
            inp_el.draw()

    def _update(self):
        pass


SETTINGS_UI = Settings()
