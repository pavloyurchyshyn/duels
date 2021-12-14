from settings.UI_setings.menus_settings.round_pause import PAUSE_MAIN_SCREEN_COPY
from settings.game_stages_constants import MAIN_MENU_STAGE

from settings.window_settings import MAIN_SCREEN, MAIN_SCREEN_DEF_COLOR

from world_arena.base.arena_cell import ArenaCell

from objects.dummy import Dummy
from spells.spells_controller import update_spells
from settings.global_parameters import GLOBAL_SETTINGS, pause_step, pause_available
from common_things.camera import GLOBAL_CAMERA
from _thread import *
from UI.UI_menus.round_pause import ROUND_PAUSE_UI
from UI.UI_menus.loading_menu import LOADING_MENU_UI
from UI.UI_buttons.round_pause import ROUND_PAUSE_BUTTON

from visual.visual_effects_controller import VisualEffectsController

from common_things.stages import Stages
from common_things.global_keyboard import GLOBAL_KEYBOARD
from common_things.global_clock import ROUND_CLOCK
from common_things.global_mouse import GLOBAL_MOUSE
from common_things.sound_loader import GLOBAL_MUSIC_PLAYER
from common_things.global_messager import GLOBAL_MESSAGER

from common_things.loggers import LOGGER
from player.commands_player import Player
import time


class SingleStage:
    def __init__(self):
        self.STAGE_CONTROLLER = Stages()
        self._ARENA = None
        self._PLAYER: Player = None
        self._round_clock = ROUND_CLOCK

        self._keyboard = GLOBAL_KEYBOARD
        self._mouse = GLOBAL_MOUSE

        self._global_messager = GLOBAL_MESSAGER

    def ROUND_PAUSE(self):
        # VisualEffectsController.update()

        if GLOBAL_KEYBOARD.ESC and pause_available():
            pause_step()
            self.STAGE_CONTROLLER.set_round_stage()

        ROUND_PAUSE_UI.update()
        ROUND_PAUSE_UI.draw()

        if self.STAGE_CONTROLLER.current_stage == MAIN_MENU_STAGE:
            del self._ARENA
            self._ARENA = None
            self._PLAYER = None
            GLOBAL_CAMERA.unfollow_player()

    def ROUND(self):
        """Just inside cell"""
        self._ARENA.draw()
        self._ARENA.update()
        VisualEffectsController.update()

        VisualEffectsController.draw_layer(0)

        self._PLAYER.update(commands=self._keyboard.commands,
                            mouse=self._mouse.pressed,
                            mouse_pos=self._mouse.pos)
        GLOBAL_CAMERA.update()
        self._DUMMY.update()
        self._PLAYER.draw()
        self._DUMMY.draw()
        update_spells()
        VisualEffectsController.draw_layer(1)

        if GLOBAL_KEYBOARD.ESC and pause_available():
            pause_step()
            PAUSE_MAIN_SCREEN_COPY.blit(MAIN_SCREEN, (0, 0))

            ROUND_PAUSE_UI.draw_round()
            self.STAGE_CONTROLLER.set_round_pause_stage()

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
            GLOBAL_CAMERA.follow_player(self._PLAYER)
            self._DUMMY = Dummy(600, 600, arena=self._ARENA)
            self._round_clock.reload()
            time.sleep(0)
        except Exception as e:
            self.STAGE_CONTROLLER.set_main_menu_stage()
            self._global_messager.add_message(text='Failed to load round')
            self._global_messager.add_message(text=f'{e}')
            LOGGER.error('Failed to load round')
            LOGGER.error(e)
        else:
            self.STAGE_CONTROLLER.set_round_stage()


SINGLE_STAGE = SingleStage()
