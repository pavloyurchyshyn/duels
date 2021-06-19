from settings.global_parameters import GLOBAL_SETTINGS, pause_step, pause_available
from settings.game_stages import CURRENT_STAGE, MAIN_MENU_S, MAIN_MENU_SETTINGS_S, \
    START_ROUND_S, ROUND_PAUSE_S, ROUND_S, \
    MULTIPLAYER_S, MULTIPLAYER_CLIENT_S, MULTIPLAYER_HOST_S, \
    EXIT_S

from UI.UI_menus.main_menu import MAIN_MENU_UI
from UI.UI_menus.main_menu_settings import MAIN_MENU_SETTINGS_UI
from UI.UI_menus.round_pause import ROUND_PAUSE_UI
from UI.UI_menus.multiplayer import MULTIPLAYER_UI
from UI.UI_buttons.round_pause import ROUND_PAUSE_BUTTON

from world_arena.world import GLOBAL_WORLD
from player_and_spells.player.commands_player import Player

from common_things.global_keyboard import GLOBAL_KEYBOARD
from common_things.global_clock import ROUND_CLOCK
from common_things.global_mouse import GLOBAL_MOUSE
from common_things.sound_loader import GLOBAL_MUSIC_PLAYER

from pygame.constants import K_F4, K_LALT
import sys
import os

from pygame import quit as close_program_pygame


class GameBody:
    def __init__(self):
        self.stages = {
            MAIN_MENU_S: self.MAIN_MENU,
            MAIN_MENU_SETTINGS_S: self.MAIN_MENU_SETTINGS,
            START_ROUND_S: self.PREPARE_TO_ROUND,

            ROUND_S: self.ROUND,
            ROUND_PAUSE_S: self.ROUND_PAUSE,

            MULTIPLAYER_S: self.MULTIPLAYER,
            EXIT_S: self.EXIT,
        }
        self._g_settings = GLOBAL_SETTINGS

        self._keyboard = GLOBAL_KEYBOARD
        self._mouse = GLOBAL_MOUSE

        self._WORLD = GLOBAL_WORLD

        self._CURRENT_CELL = None
        self._PLAYER = Player(500, 500)
        self._round_clock = ROUND_CLOCK

        self._music_player = GLOBAL_MUSIC_PLAYER
        self._music_player.play_back_music()

    def game_loop(self):
        """
        Main part of game. Runs stages.
        """
        self._music_player.update()
        self.stages[self._g_settings[CURRENT_STAGE]]()
        self._check_alt_and_f4()

    def ROUND_PAUSE(self):
        self._CURRENT_CELL.draw()
        self._PLAYER.draw()
        if GLOBAL_KEYBOARD.ESC and pause_available():
            pause_step()
            self._g_settings[CURRENT_STAGE] = ROUND_S

        ROUND_PAUSE_UI.update()
        ROUND_PAUSE_UI.draw()

    def ROUND(self):
        """Just inside cell"""
        self._keyboard.update()

        self._CURRENT_CELL.update()
        self._CURRENT_CELL.draw()

        self._PLAYER.update(commands=self._keyboard.commands,
                            mouse=self._mouse.pressed,
                            mouse_pos=self._mouse.pos)
        self._PLAYER.draw()

        if GLOBAL_KEYBOARD.ESC and pause_available():
            pause_step()
            self._g_settings[CURRENT_STAGE] = ROUND_PAUSE_S

        ROUND_PAUSE_BUTTON.draw()
        if GLOBAL_MOUSE.lmb:
            xy = GLOBAL_MOUSE.pos
            ROUND_PAUSE_BUTTON.click(xy)

    def PREPARE_TO_ROUND(self):
        self._round_clock.reload()
        self._g_settings[CURRENT_STAGE] = ROUND_S
        self._WORLD.build_cell()
        self._CURRENT_CELL = self._WORLD.GET_CURRENT_CELL()
        self._PLAYER.update_cell(self._CURRENT_CELL)

    def MAIN_MENU(self) -> None:
        """
        Main menu logic.
        """
        MAIN_MENU_UI.update()
        MAIN_MENU_UI.draw()

    def MAIN_MENU_SETTINGS(self):
        MAIN_MENU_SETTINGS_UI.update()
        MAIN_MENU_SETTINGS_UI.draw()

    def _check_alt_and_f4(self):
        # TODO if in round -> save game
        pressed = self._keyboard.pressed
        if pressed[K_F4] and pressed[K_LALT]:
            self._close_game()

    def MULTIPLAYER(self):
        if GLOBAL_KEYBOARD.ESC and pause_available():
            pause_step()
            self._g_settings[CURRENT_STAGE] = MAIN_MENU_S

        MULTIPLAYER_UI.update()
        MULTIPLAYER_UI.draw()

    def EXIT(self):
        self._close_game()

    def _close_game(self):
        close_program_pygame()
        sys.exit()
