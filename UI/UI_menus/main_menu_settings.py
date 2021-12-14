from UI.UI_base.menu_UI import MenuUI
from common_things.camera import GLOBAL_CAMERA
from common_things.global_mouse import GLOBAL_MOUSE
from common_things.global_keyboard import GLOBAL_KEYBOARD

from settings.UI_setings.menus_settings.main_menu_settings import MAIN_MENU_SETTINGS_BUTTONS, \
    MUSIC_VOLUME_VALUE, VOLUME_PROGRESS_BAR, MUTE_MUSIC_BUTTON, PLAYER_PIC, COLORS_INPUTS_LIST

from settings.global_parameters import pause_available, pause_step
from common_things.stages import Stages

from settings.game_stages_constants import MAIN_MENU_SETTINGS_STAGE

set_main_menu_stage = Stages().set_main_menu_stage


class MainMenuSettings(MenuUI):
    def __init__(self):
        super().__init__(buttons=MAIN_MENU_SETTINGS_BUTTONS, name=MAIN_MENU_SETTINGS_STAGE)
        self.create_buttons()

        self._chosen_button = None
        self._music_volume_value = MUSIC_VOLUME_VALUE
        self.add_elements_to_controller(*self._buttons, *COLORS_INPUTS_LIST, MUTE_MUSIC_BUTTON)

    def update(self):

        for inp_el in COLORS_INPUTS_LIST:
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

        PLAYER_PIC.update()
        GLOBAL_CAMERA.set_dx_dy(0, 0)

    def draw(self, dx=0, dy=0):
        self._draw(dx, dy)
        self._music_volume_value.draw(dx, dy)
        VOLUME_PROGRESS_BAR.draw(dx, dy)
        MUTE_MUSIC_BUTTON.draw(dx, dy)
        PLAYER_PIC.draw()
        for element in COLORS_INPUTS_LIST:
            element.draw()

    def _update(self):
        pass


MAIN_MENU_SETTINGS_UI = MainMenuSettings()
