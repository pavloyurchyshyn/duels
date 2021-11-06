from _thread import *

from settings.global_parameters import GLOBAL_SETTINGS, pause_step, pause_available
from settings.window_settings import MAIN_SCREEN, MAIN_SCREEN_DEF_COLOR
from settings.UI_setings.menus_settings.round_pause import PAUSE_MAIN_SCREEN_COPY

from settings.game_stages_constants import CURRENT_STAGE, MAIN_MENU_STAGE, MAIN_MENU_SETTINGS_STAGE, \
    START_ROUND_STAGE, ROUND_PAUSE_STAGE, ROUND_STAGE, \
    MULTIPLAYER_MENU_STAGE, MULTIPLAYER_CLIENT_DISCONNECT_STAGE, \
    MULTIPLAYER_CLIENT_ROUND_PAUSE_STAGE, MULTIPLAYER_CLIENT_ROUND_STAGE, \
    HOST_SERVER_STAGE, EXIT_STAGE, MULTIPLAYER_CLIENT_CONNECT_ROUND_STAGE, LOADING_STAGE

from UI.UI_controller import UI_TREE
from UI.UI_menus.main_menu import MAIN_MENU_UI
from UI.UI_menus.main_menu_settings import MAIN_MENU_SETTINGS_UI
from UI.UI_menus.round_pause import ROUND_PAUSE_UI
from UI.UI_menus.multiplayer import MULTIPLAYER_UI
from UI.UI_menus.mul_round_pause import MUL_ROUND_PAUSE_UI
from UI.UI_menus.loading_menu import LOADING_MENU_UI
from UI.UI_buttons.round_pause import ROUND_PAUSE_BUTTON

from world_arena.base.arena_cell import ArenaCell

from player_and_spells.player.commands_player import Player

from common_things.stages import Stages
from common_things.global_keyboard import GLOBAL_KEYBOARD
from common_things.global_clock import ROUND_CLOCK
from common_things.global_mouse import GLOBAL_MOUSE
from common_things.sound_loader import GLOBAL_MUSIC_PLAYER
from common_things.global_messager import GLOBAL_MESSAGER

from network.server_controller import SERVER_CONTROLLER

from pygame.constants import K_F4, K_LALT
import sys
import os

from game_stages_classes.multiplayer_stage import GLOBAL_MUL_STAGE

from pygame import quit as close_program_pygame

from time import sleep


class GameBody:
    def __init__(self):
        self.stages = {
            MAIN_MENU_STAGE: self.MAIN_MENU,
            MAIN_MENU_SETTINGS_STAGE: self.MAIN_MENU_SETTINGS,
            START_ROUND_STAGE: self.PREPARE_TO_ROUND,

            ROUND_STAGE: self.ROUND,
            ROUND_PAUSE_STAGE: self.ROUND_PAUSE,

            MULTIPLAYER_MENU_STAGE: self.MULTIPLAYER_MENU,
            HOST_SERVER_STAGE: self.HOST_SERVER,  # run to create server

            MULTIPLAYER_CLIENT_CONNECT_ROUND_STAGE: self.MULTIPLAYER_CLIENT_CONNECT,
            MULTIPLAYER_CLIENT_ROUND_STAGE: self.MULTIPLAYER_CLIENT_ROUND,
            MULTIPLAYER_CLIENT_ROUND_PAUSE_STAGE: self.MULTIPLAYER_CLIENT_ROUND_PAUSE,
            MULTIPLAYER_CLIENT_DISCONNECT_STAGE: self.MULTIPLAYER_CLIENT_DISCONNECT,

            LOADING_STAGE: self.LOADING,

            EXIT_STAGE: self.EXIT,

        }
        self._fill_screen_stages = {}

        self._g_settings = GLOBAL_SETTINGS

        self._keyboard = GLOBAL_KEYBOARD
        self._mouse = GLOBAL_MOUSE

        self._ARENA = None
        self._PLAYER: Player = None
        self._round_clock = ROUND_CLOCK

        self._music_player = GLOBAL_MUSIC_PLAYER
        self._music_player.play_back_music()

        self._global_messager = GLOBAL_MESSAGER

        self.STAGE_CONTROLLER = Stages()

    def game_loop(self):
        """
        Main part of game. Runs stages.
        """
        if self.STAGE_CONTROLLER.current_stage in self._fill_screen_stages:
            MAIN_SCREEN.fill(MAIN_SCREEN_DEF_COLOR)

        self._music_player.update()
        self.stages[self.STAGE_CONTROLLER.current_stage]()
        self._check_alt_and_f4()
        self._global_messager.update()
        self._global_messager.draw()
        UI_TREE.update()
        UI_TREE.draw()

    def ROUND_PAUSE(self):
        if GLOBAL_KEYBOARD.ESC and pause_available():
            pause_step()
            self.STAGE_CONTROLLER.set_round_stage()

        ROUND_PAUSE_UI.update()
        ROUND_PAUSE_UI.draw()
        if GLOBAL_SETTINGS[CURRENT_STAGE] == MAIN_MENU_STAGE:
            del self._ARENA
            self._ARENA = None
            self._PLAYER = None

    def ROUND(self):
        """Just inside cell"""
        self._ARENA.draw()
        self._ARENA.update()

        self._PLAYER.update(commands=self._keyboard.commands,
                            mouse=self._mouse.pressed,
                            mouse_pos=self._mouse.pos)
        self._PLAYER.draw()

        if GLOBAL_KEYBOARD.ESC and pause_available():
            pause_step()
            self.STAGE_CONTROLLER.set_round_pause_stage()
            PAUSE_MAIN_SCREEN_COPY.blit(MAIN_SCREEN, (0, 0))
            ROUND_PAUSE_UI.draw_round()

        ROUND_PAUSE_BUTTON.draw()
        if GLOBAL_MOUSE.lmb:
            ROUND_PAUSE_BUTTON.click(GLOBAL_MOUSE.pos)

    def PREPARE_TO_ROUND(self):
        start_new_thread(self.__load_round, (self,))
        self.STAGE_CONTROLLER.set_loading_stage()

    def LOADING(self):
        LOADING_MENU_UI.update()
        LOADING_MENU_UI.draw()

    @staticmethod
    def __load_round(self):
        try:
            self._ARENA = ArenaCell({}, draw_grid=True)
            self._PLAYER = Player(500, 500, arena=self._ARENA)
            self._round_clock.reload()
        except Exception as e:
            self.STAGE_CONTROLLER.set_main_menu_stage()
            self._global_messager.add_message(text='Failed to load round')
            self._global_messager.add_message(text=f'{e}')
        else:
            self.STAGE_CONTROLLER.set_round_stage()

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

    def MULTIPLAYER_MENU(self):
        if GLOBAL_KEYBOARD.ESC and pause_available():
            pause_step()
            self.STAGE_CONTROLLER.set_main_menu_stage()

        MULTIPLAYER_UI.update()
        MULTIPLAYER_UI.draw()

    def HOST_SERVER(self):
        SERVER_CONTROLLER.run_server()
        if GLOBAL_KEYBOARD.ESC and pause_available():
            pause_step()
            self.STAGE_CONTROLLER.set_multiplayers_disconnect_stage()

        self.STAGE_CONTROLLER.set_multiplayer_client_connect_round_stage()

    @staticmethod
    def MULTIPLAYER_CLIENT_CONNECT():
        GLOBAL_MUL_STAGE.MULTIPLAYER_CLIENT_CONNECT()

    @staticmethod
    def MULTIPLAYER_CLIENT_ROUND():
        GLOBAL_MUL_STAGE.UPDATE()

    def MULTIPLAYER_CLIENT_ROUND_PAUSE(self):
        if GLOBAL_KEYBOARD.ESC and pause_available():
            pause_step()
            self._g_settings[CURRENT_STAGE] = MULTIPLAYER_CLIENT_ROUND_STAGE

        GLOBAL_MUL_STAGE.UPDATE(pause=True)
        MUL_ROUND_PAUSE_UI.update()
        MUL_ROUND_PAUSE_UI.draw()

    @staticmethod
    def MULTIPLAYER_CLIENT_DISCONNECT():
        GLOBAL_MUL_STAGE.MULTIPLAYER_CLIENT_DISCONNECT()

    def EXIT(self):
        self._close_game()

    def _close_game(self):
        self.MULTIPLAYER_CLIENT_DISCONNECT()

        close_program_pygame()
        sys.exit()
