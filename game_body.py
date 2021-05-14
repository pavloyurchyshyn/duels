from settings.global_parameters import GLOBAL_SETTINGS
from settings.game_stages import CURRENT_STAGE, MAIN_MENU_S, MAIN_MENU_SETTINGS_S

from UI.UI_menus.main_menu import MAIN_MENU_UI

from common_things.global_keyboard import GLOBAL_KEYBOARD
from pygame.constants import K_F4, K_LALT
import sys

from pygame import quit as QUIT


class GameBody:
    def __init__(self):
        self.stages = {
            MAIN_MENU_S: self.MAIN_MENU,
            MAIN_MENU_SETTINGS_S: self.MAIN_MENU_SETTINGS,
        }
        self._g_settings = GLOBAL_SETTINGS

        self._keyboard = GLOBAL_KEYBOARD

    def game_loop(self):
        """
        Main part of game. Runs stages.

        :return:
        """
        self.stages[self._g_settings[CURRENT_STAGE]]()
        self._check_alt_and_f4()

    def ROUND(self):
        """Just inside cell"""
        pass

    def GLOBAL_MAP(self):
        """Choose were to go"""
        pass

    def MAIN_MENU(self) -> None:
        """
        Main menu logic.

        :return:
        """
        MAIN_MENU_UI.update()
        MAIN_MENU_UI.draw()

    def MAIN_MENU_SETTINGS(self):
        self._close_game()

    def _check_alt_and_f4(self):
        pressed = self._keyboard.pressed
        if pressed[K_F4] and pressed[K_LALT]:
            self._close_game()

    def _close_game(self):
        QUIT()
        sys.exit()
