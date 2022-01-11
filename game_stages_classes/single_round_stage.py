from _thread import *
import time

from settings.UI_setings.menus_settings.round_pause import PAUSE_MAIN_SCREEN_COPY
from settings.game_stages_constants import MAIN_MENU_STAGE
from settings.window_settings import MAIN_SCREEN
from settings.global_parameters import pause_step, pause_available

from world_arena.base.arena_cell import ArenaCell

from objects.dummy import Dummy
from objects.ball import Ball
from objects.gates import BallGate

from spells.spells_controller import update_spells

from UI.UI_menus.round_pause import ROUND_PAUSE_UI
from UI.UI_menus.loading_menu import LOADING_MENU_UI
from UI.UI_buttons.round_pause import ROUND_PAUSE_BUTTON
from UI.player_bot_bar import PlayerBotBar
from UI.global_messager import GLOBAL_MESSAGER
from UI.ball_arrow import BallArrow

from visual.base.visual_effects_controller import VisualEffectsController

from common_things.stages import Stages
from common_things.global_keyboard import GLOBAL_KEYBOARD
from common_things.global_clock import ROUND_CLOCK
from common_things.global_mouse import GLOBAL_MOUSE
from common_things.common_objects_lists_dicts import OBJECTS_LIST, PLAYERS_LIST
from common_things.camera import GLOBAL_CAMERA
from common_things.global_round_parameters import GLOBAL_ROUND_PARAMETERS
from common_things.loggers import LOGGER

from player.client_player import Player


class SingleStage:
    def __init__(self):
        self.global_round_parameters = GLOBAL_ROUND_PARAMETERS
        self.STAGE_CONTROLLER = Stages()
        self._ARENA = None
        self._PLAYER: Player = None
        self._round_clock = ROUND_CLOCK

        self._keyboard = GLOBAL_KEYBOARD
        self._mouse = GLOBAL_MOUSE

        self._global_messager = GLOBAL_MESSAGER
        self._player_bot_bar: PlayerBotBar = None
        self._ball = None
        self._gates = []

        self._ball_arrow = None

    def ROUND_PAUSE(self):
        if GLOBAL_KEYBOARD.ESC and pause_available():
            pause_step()
            self.STAGE_CONTROLLER.set_round_stage()

        ROUND_PAUSE_UI.update()
        ROUND_PAUSE_UI.draw()

        if self.STAGE_CONTROLLER.current_stage == MAIN_MENU_STAGE:
            del self._ARENA
            self.close_round_stage()

    def ROUND(self):
        """Just inside cell"""
        self._ARENA.draw()
        self._ARENA.update()
        VisualEffectsController.update()

        VisualEffectsController.draw_layer(0)
        m_click = self._mouse.lmb
        if m_click and ROUND_PAUSE_BUTTON.collide_point(self._mouse.pos):
            self._mouse.lmb = 0

        self._PLAYER.update(commands=self._keyboard.commands,
                            mouse=self._mouse.pressed,
                            mouse_pos=self._mouse.pos)
        GLOBAL_CAMERA.update()
        self._PLAYER.draw()

        self._ball.update()
        self._ball_arrow.update()

        for gate in self._gates:
            gate.update()
            gate.draw()

        self._ball.draw()

        update_spells()
        VisualEffectsController.draw_layer(1)

        if GLOBAL_KEYBOARD.ESC and pause_available():
            pause_step()
            PAUSE_MAIN_SCREEN_COPY.blit(MAIN_SCREEN, (0, 0))

            ROUND_PAUSE_UI.draw_round()
            self.STAGE_CONTROLLER.set_round_pause_stage()

        ROUND_PAUSE_BUTTON.draw()

        self._player_bot_bar.update()
        self._player_bot_bar.draw()
        self._ball_arrow.draw()

        if m_click:
            ROUND_PAUSE_BUTTON.click(GLOBAL_MOUSE.pos)

    def PREPARE_TO_ROUND(self):
        start_new_thread(self.__load_round, (self,))
        self.STAGE_CONTROLLER.set_loading_stage()

    def LOADING(self):
        LOADING_MENU_UI.update()
        LOADING_MENU_UI.draw()

    def close_round_stage(self):
        self.STAGE_CONTROLLER.set_main_menu_stage()
        self.global_round_parameters.reload()
        self._PLAYER = None
        self._ARENA = None
        self._gates.clear()
        self._ball = None
        self._player_bot_bar = None
        self._ball_arrow = None

        self._round_clock.reload()
        PLAYERS_LIST.clear()

        GLOBAL_CAMERA.unfollow_player()

    @staticmethod
    def __load_round(self):
        try:
            PLAYERS_LIST.clear()
            self._ARENA = ArenaCell({}, draw_grid=True)
            self._gates.append(BallGate(x=0, y=self._ARENA.center[1], direction_right=1))
            self._gates.append(BallGate(x=self._ARENA.size_x, y=self._ARENA.center[1], direction_right=0))

            self._ball = Ball(start_pos=self._ARENA.center, arena=self._ARENA)
            self.global_round_parameters.ball = self._ball

            self._ball_arrow = BallArrow()
            self._ball_arrow.follow_ball(self._ball)

            self._PLAYER = Player(500, 500, arena=self._ARENA)
            self.global_round_parameters.arena = self._ARENA

            self._player_bot_bar = PlayerBotBar(self._PLAYER)
            GLOBAL_CAMERA.follow_player(self._PLAYER)
            self._round_clock.reload()

            OBJECTS_LIST.append(Dummy(600, 600, arena=self._ARENA, camera=GLOBAL_CAMERA))

            time.sleep(1)
        except Exception as e:
            self._global_messager.add_message(text='Failed to load round')
            self._global_messager.add_message(text=f'{e}')
            LOGGER.error('Failed to load round')
            LOGGER.error(e)
            self.close_round_stage()
        else:
            self.STAGE_CONTROLLER.set_round_stage()

    def __del__(self):
        self.close_round_stage()


SINGLE_STAGE = SingleStage()
