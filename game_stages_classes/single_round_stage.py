from _thread import *
import time

from settings.UI_setings.menus_settings.round_pause import PAUSE_MAIN_SCREEN_COPY
from settings.game_stages_constants import MAIN_MENU_STAGE
from settings.window_settings import MAIN_SCREEN
from settings.global_parameters import pause_step, pause_available, set_slow_motion

from world_arena.base.arena_cell import ArenaCell

from objects.dummy import Dummy
from objects.ball import Ball
from objects.gates import BallGate
from objects.turret import Turret

from UI.UI_menus.round_pause import ROUND_PAUSE_UI
from UI.UI_menus.loading_menu import LOADING_MENU_UI
from UI.UI_buttons.round_pause import ROUND_PAUSE_BUTTON
from UI.player_bot_bar import PlayerBotBar
from UI.global_messager import GLOBAL_MESSAGER
from UI.ball_arrow import BallArrow
from UI.scores_text import ScoresText
from UI.UI_buttons.slow_motion_button import SLOW_MOTION_BUTTON

from visual.base.visual_effects_controller import VisualEffectsController
from visual.simple_hit_effect import base_hit_effect_func

from common_things.stages import Stages
from common_things.global_keyboard import GLOBAL_KEYBOARD
from common_things.global_clock import ROUND_CLOCK
from common_things.global_mouse import GLOBAL_MOUSE
from common_things.common_objects_lists_dicts import OBJECTS_LIST, PLAYERS_DICT
from common_things.camera import GLOBAL_CAMERA
from common_things.global_round_parameters import GLOBAL_ROUND_PARAMETERS
from common_things.loggers import LOGGER

from object_controller import AllObjectsController

from player.client_player import Player

import traceback


class SingleStage:
    def __init__(self):
        self.global_round_parameters = GLOBAL_ROUND_PARAMETERS
        self.STAGE_CONTROLLER = Stages()
        self._ARENA: ArenaCell = None
        self._PLAYER: Player = None
        self._round_clock = ROUND_CLOCK

        self._keyboard = GLOBAL_KEYBOARD
        self._mouse = GLOBAL_MOUSE

        self._global_messager = GLOBAL_MESSAGER
        self._player_bot_bar: PlayerBotBar = None
        self._ball: Ball = None
        self._gates: [BallGate, BallGate] = []

        self._ball_arrow: BallArrow = None
        self._objects_controller: AllObjectsController = None

        self._scores = self.global_round_parameters.scores
        self._scores_text = ScoresText(self.global_round_parameters.scores)
        self._scores_text.update_text()

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
        self._ball.draw()

        self._objects_controller.update()

        VisualEffectsController.update()
        VisualEffectsController.draw_layer(0)

        SLOW_MOTION_BUTTON.update()
        ROUND_PAUSE_BUTTON.update()

        m_click = self._mouse.lmb
        if m_click and (ROUND_PAUSE_BUTTON.collide_point(self._mouse.pos) or SLOW_MOTION_BUTTON.collide_point(self._mouse.pos)):
            self._mouse.lmb = 0

        self._PLAYER.update(commands=self._keyboard.commands,
                            mouse=self._mouse.pressed,
                            mouse_pos=self._mouse.pos)
        GLOBAL_CAMERA.update()
        self._PLAYER.draw()

        self._ball.update()
        self.check_for_goal()
        self._ball_arrow.update()

        for gate in self._gates:
            gate.update()
            gate.draw()

        VisualEffectsController.draw_layer(1)

        if GLOBAL_KEYBOARD.ESC and pause_available():
            pause_step()
            PAUSE_MAIN_SCREEN_COPY.blit(MAIN_SCREEN, (0, 0))

            ROUND_PAUSE_UI.draw_round()
            self.STAGE_CONTROLLER.set_round_pause_stage()

        self._player_bot_bar.update()
        self._player_bot_bar.draw()
        self._ball_arrow.draw()
        self._scores_text.draw()

        SLOW_MOTION_BUTTON.draw()
        ROUND_PAUSE_BUTTON.draw()

        if m_click:
            ROUND_PAUSE_BUTTON.click(GLOBAL_MOUSE.pos)
            SLOW_MOTION_BUTTON.click(GLOBAL_MOUSE.pos)

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
        if self._objects_controller:
            self._objects_controller.clear()
        self._objects_controller = None
        self._scores_text = None
        self._round_clock.reload()
        PLAYERS_DICT.clear()
        self._scores.clear()

        GLOBAL_CAMERA.unfollow_player()

    def check_for_goal(self):
        for gate in self._gates:
            if gate.collide(self._ball):
                if gate.collide_borders(self._ball):
                    self._ball.reverse_vertical()
                    break

                else:
                    self._scores[gate.team] += 1
                    self._scores_text.update_text()
                    base_hit_effect_func(1, *self._ball.get_pos(), -self._ball._angle)

                    self._ball.reload()
                    set_slow_motion()
                    break

    @staticmethod
    def __load_round(self):
        try:
            PLAYERS_DICT.clear()
            self._ARENA = ArenaCell({}, draw_grid=True)
            LOGGER.info(f"Created arena: {self._ARENA.__dict__}")
            self._objects_controller = AllObjectsController(self._ARENA)

            self._scores['red'] = 0
            self._scores['blue'] = 0

            self._scores_text = ScoresText(self.global_round_parameters.scores)
            self._scores_text.update_text()

            self._gates.append(BallGate(x=self._ARENA._border_size, y=self._ARENA.center[1],
                                        direction_right=1, team='red'))
            self._gates.append(BallGate(x=self._ARENA.size_x - self._ARENA._border_size, y=self._ARENA.center[1],
                                        direction_right=0, team='blue'))

            self._ball = Ball(start_pos=self._ARENA.center, arena=self._ARENA)
            LOGGER.info(f"Created player: {self._ball.__dict__}")

            self.global_round_parameters.ball = self._ball

            self._ball_arrow = BallArrow()
            self._ball_arrow.follow_ball(self._ball)

            self._PLAYER = Player(1000, 1000, arena=self._ARENA)
            LOGGER.info(f"Created player: {self._PLAYER.__dict__}")

            self.global_round_parameters.arena = self._ARENA

            self._player_bot_bar = PlayerBotBar(self._PLAYER)
            GLOBAL_CAMERA.follow_player(self._PLAYER)
            GLOBAL_CAMERA.update()
            self._round_clock.reload()

            OBJECTS_LIST.append(Dummy(600, 600, arena=self._ARENA, camera=GLOBAL_CAMERA))
            OBJECTS_LIST.append(Turret(500, 500))

            # time.sleep(2)

        except Exception as e:
            self._global_messager.add_message(text='Failed to load round')
            self._global_messager.add_message(text=f'{e}')
            LOGGER.error('Failed to load round')
            LOGGER.error(e)
            LOGGER.error(traceback.format_exc())
            self.close_round_stage()
        else:
            self.STAGE_CONTROLLER.set_round_stage()

    def __del__(self):
        self.close_round_stage()


SINGLE_STAGE = SingleStage()
