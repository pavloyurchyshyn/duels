from settings.global_parameters import GLOBAL_SETTINGS, pause_step, pause_available

from settings.window_settings import MAIN_SCREEN, MAIN_SCREEN_DEF_COLOR
from settings.UI_setings.menus_settings.round_pause import PAUSE_MAIN_SCREEN_COPY
from settings.screen_size import SCREEN_H, SCREEN_W, Y_SCALE, X_SCALE
from settings.game_stages import CURRENT_STAGE, MAIN_MENU_S, MAIN_MENU_SETTINGS_S, \
    START_ROUND_S, ROUND_PAUSE_S, ROUND_S, \
    MULTIPLAYER_MENU_S, MULTIPLAYER_CLIENT_DISCONNECT_S, \
    MULTIPLAYER_CLIENT_ROUND_PAUSE_S, MULTIPLAYER_CLIENT_ROUND_S, \
    MULTIPLAYER_CLIENT_S, MULTIPLAYER_HOST_S, HOST_SERVER, \
    EXIT_S, MULTIPLAYER_CLIENT_CONNECT_ROUND_S
from settings.network_settings import CHANGE_CONNECTION, DELETE_PLAYERS, SERVER_ACTION, DELETE_PLAYER, PLAYERS_DATA, SERVER_TIME

from UI.UI_menus.main_menu import MAIN_MENU_UI
from UI.UI_menus.main_menu_settings import MAIN_MENU_SETTINGS_UI
from UI.UI_menus.round_pause import ROUND_PAUSE_UI
from UI.UI_menus.multiplayer import MULTIPLAYER_UI
from UI.UI_menus.mul_round_pause import MUL_ROUND_PAUSE_UI
from UI.UI_buttons.round_pause import ROUND_PAUSE_BUTTON
from UI.UI_base.messages_UI import Messager

from world_arena.world import GLOBAL_WORLD
from world_arena.base.arena_cell import ArenaCell

from player_and_spells.player.commands_player import Player
from player_and_spells.player.simple_player import SimplePlayer

from common_things.global_keyboard import GLOBAL_KEYBOARD
from common_things.global_clock import ROUND_CLOCK
from common_things.global_mouse import GLOBAL_MOUSE
from common_things.sound_loader import GLOBAL_MUSIC_PLAYER
from common_things.global_messager import GLOBAL_MESSAGER
from common_things.loggers import LOGGER
from common_things.save_and_load_json_config import save_param_to_cgs, get_param_from_cgs
from network.network import Network
from network.server_controller import SERVER_CONTROLLER

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

            MULTIPLAYER_MENU_S: self.MULTIPLAYER_MENU,
            HOST_SERVER: self.HOST_SERVER,  # run if to create server
            MULTIPLAYER_CLIENT_CONNECT_ROUND_S: self.MULTIPLAYER_CLIENT_CONNECT,
            MULTIPLAYER_CLIENT_ROUND_S: self.MULTIPLAYER_CLIENT_ROUND,
            MULTIPLAYER_CLIENT_ROUND_PAUSE_S: self.MULTIPLAYER_CLIENT_ROUND_PAUSE,
            MULTIPLAYER_CLIENT_DISCONNECT_S: self.MULTIPLAYER_CLIENT_DISCONNECT,

            EXIT_S: self.EXIT,

        }
        self._fill_screen_stages = {}

        self._g_settings = GLOBAL_SETTINGS

        self._keyboard = GLOBAL_KEYBOARD
        self._mouse = GLOBAL_MOUSE

        self._WORLD = GLOBAL_WORLD

        self._CURRENT_CELL = None
        self._PLAYER = None
        self._round_clock = ROUND_CLOCK

        self._music_player = GLOBAL_MUSIC_PLAYER
        self._music_player.play_back_music()

        self._server_controller = None
        self._network: Network = None
        self._network_address_key = None
        self._multiplayer_cell = None
        self._multiplayer_player: Player = None
        self._other_multiplayer_players: dict = {}
        self._network_last_data = {}
        self._static_client_data = {}
        self._global_messager = GLOBAL_MESSAGER

    def game_loop(self):
        """
        Main part of game. Runs stages.
        """
        if CURRENT_STAGE in self._fill_screen_stages:
            MAIN_SCREEN.fill(MAIN_SCREEN_DEF_COLOR)

        self._music_player.update()
        self.stages[self._g_settings[CURRENT_STAGE]]()
        self._check_alt_and_f4()
        self._global_messager.update()
        self._global_messager.draw()

    def ROUND_PAUSE(self):
        if GLOBAL_KEYBOARD.ESC and pause_available():
            pause_step()
            self._g_settings[CURRENT_STAGE] = ROUND_S

        ROUND_PAUSE_UI.update()
        ROUND_PAUSE_UI.draw()

    def ROUND(self):
        """Just inside cell"""

        self._CURRENT_CELL.update()
        self._CURRENT_CELL.draw()

        self._PLAYER.update(commands=self._keyboard.commands,
                            mouse=self._mouse.pressed,
                            mouse_pos=self._mouse.pos)
        self._PLAYER.draw()

        if GLOBAL_KEYBOARD.ESC and pause_available():
            pause_step()
            self._g_settings[CURRENT_STAGE] = ROUND_PAUSE_S
            PAUSE_MAIN_SCREEN_COPY.blit(MAIN_SCREEN, (0, 0))
            ROUND_PAUSE_UI.draw_round()

        ROUND_PAUSE_BUTTON.draw()
        if GLOBAL_MOUSE.lmb:
            xy = GLOBAL_MOUSE.pos
            ROUND_PAUSE_BUTTON.click(xy)

    def PREPARE_TO_ROUND(self):
        self._PLAYER = Player(500, 500)
        self._round_clock.reload()
        self._g_settings[CURRENT_STAGE] = ROUND_S
        self._WORLD.build_cell()
        self._CURRENT_CELL = ArenaCell({}, draw_grid=True)
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

    def MULTIPLAYER_MENU(self):
        if GLOBAL_KEYBOARD.ESC and pause_available():
            pause_step()
            self._g_settings[CURRENT_STAGE] = MAIN_MENU_S

        MULTIPLAYER_UI.update()
        MULTIPLAYER_UI.draw()

    def HOST_SERVER(self):
        SERVER_CONTROLLER.run_server()
        if GLOBAL_KEYBOARD.ESC and pause_available():
            pause_step()
            self._g_settings[CURRENT_STAGE] = MULTIPLAYER_CLIENT_DISCONNECT_S

        self._g_settings[CURRENT_STAGE] = MULTIPLAYER_CLIENT_CONNECT_ROUND_S

    def MULTIPLAYER_CLIENT_CONNECT(self):
        self._network = Network()
        res = self._network.connect()

        if self._network.connected:
            self._global_messager.add_message(res.get('server_msg'))
            self._network_address_key = str(res.get('network_address_key'))
            self._g_settings[CURRENT_STAGE] = MULTIPLAYER_CLIENT_ROUND_S
            data = {}
            self._multiplayer_cell = ArenaCell(data, draw_grid=True)

            x, y = res.get('position', (100, 100))
            self._multiplayer_player = Player(x=int(x * X_SCALE), y=int(y * Y_SCALE))
            self._multiplayer_player.position = res.get('position')
            self._multiplayer_player.angle = res.get('angle')
            self._multiplayer_player.hp = res.get('hp')
            self._multiplayer_player.update({}, (0, 0, 0), (0, 0))

            self._static_client_data['player_color'] = self._multiplayer_player.color

            self._other_multiplayer_players.clear()
        else:
            MULTIPLAYER_UI.network_messager.add_message(res.get('server_msg'))
            self._g_settings[CURRENT_STAGE] = MULTIPLAYER_MENU_S

    def MULTIPLAYER_CLIENT_ROUND(self):
        data_to_send = {
            'keyboard': tuple(self._keyboard.commands),
            'mouse_data': self._mouse.network_data,
            'position': self._multiplayer_player.position,
            'angle': self._multiplayer_player.angle
        }
        data_to_send.update(self._static_client_data)

        # LOGGER.info(f'Player_info: {data_to_send}')
        try:
            data = self._network.update(data=data_to_send)
            self._network_last_data = data_to_send.copy()
            data_to_send.clear()
        except Exception as e:
            LOGGER.error(e)
            self._g_settings[CURRENT_STAGE] = MULTIPLAYER_CLIENT_DISCONNECT_S
            self._global_messager.add_message('Server connection lost')

        else:
            ROUND_CLOCK.set_time(*data.pop(SERVER_TIME))

            if SERVER_ACTION in data:
                server_action = data.pop(SERVER_ACTION)
                if DELETE_PLAYERS in server_action and server_action.pop(DELETE_PLAYERS):
                    self._other_multiplayer_players.clear()

                if DELETE_PLAYER in server_action:
                    if server_action[DELETE_PLAYER] in self._other_multiplayer_players:
                        self._other_multiplayer_players.pop(server_action[DELETE_PLAYER])

            # TODO: LOGIC for update
            self._multiplayer_cell.draw()
            if PLAYERS_DATA in data and data[PLAYERS_DATA]:
                players_data = data[PLAYERS_DATA]
                if self._network_address_key in players_data:
                    p_data = players_data.pop(self._network_address_key)
                    self._multiplayer_player.position = p_data.get('position')
                    self._multiplayer_player.angle = p_data.get('angle')
                    mouse_data, mouse_pos = p_data.get('mouse_data', ((0, 0, 0), (0, 0)))
                    commands = p_data.get('keyboard', ())
                else:
                    commands = ()
                    mouse_data, mouse_pos = (0, 0, 0), (0, 0)

                self._multiplayer_player.update((), mouse=mouse_data, mouse_pos=GLOBAL_MOUSE.pos)
                self._multiplayer_player.draw()

                for addr, player in self._other_multiplayer_players.items():
                    if addr in players_data:
                        p_data = players_data.pop(addr)
                        # value = self._network.str_to_json(value)
                        commands = p_data.get('keyboard', {})
                        player.position = p_data.get('position')
                        player.angle = p_data.get('angle')
                    else:
                        commands = ()

                    player.update(commands)
                    player.draw()

                if players_data:
                    for addr, value in players_data.items():
                        player = SimplePlayer(x=200, y=200, main_player=False,
                                              player_skin=value.get('player_color'),
                                              under_circle_color=1, enemy=True)
                        self._other_multiplayer_players[str(addr)] = player

                        player.position = value.get('position')
                        player.angle = value.get('angle')
                        player.update(value.get('keyboard', {}))
                        player.draw()
                        # print(f'Created player for {addr}')

            if GLOBAL_KEYBOARD.ESC and pause_available():
                pause_step()
                self._g_settings[CURRENT_STAGE] = MULTIPLAYER_CLIENT_ROUND_PAUSE_S
                self._network_last_data['keyboard'] = {}

    def MULTIPLAYER_CLIENT_ROUND_PAUSE(self):
        if GLOBAL_KEYBOARD.ESC and pause_available():
            pause_step()
            self._g_settings[CURRENT_STAGE] = MULTIPLAYER_CLIENT_ROUND_S

        try:
            data = self._network.update(data=self._network_last_data.copy())

        except Exception as e:
            LOGGER.error(e)
            self._g_settings[CURRENT_STAGE] = MULTIPLAYER_CLIENT_DISCONNECT_S
            self._global_messager.add_message('Server connection lost')

        else:
            ROUND_CLOCK.set_time(*data.pop(SERVER_TIME))

            if SERVER_ACTION in data:
                server_action = data.pop(SERVER_ACTION)
                if DELETE_PLAYERS in server_action and server_action.pop(DELETE_PLAYERS):
                    self._other_multiplayer_players.clear()

                if DELETE_PLAYER in server_action:
                    if server_action[DELETE_PLAYER] in self._other_multiplayer_players:
                        self._other_multiplayer_players.pop(server_action[DELETE_PLAYER])

            if PLAYERS_DATA in data and data[PLAYERS_DATA]:
                players_data = data[PLAYERS_DATA]
                if self._network_address_key in players_data:
                    p_data = players_data.pop(self._network_address_key)
                    self._multiplayer_player.position = p_data.get('position')
                    self._multiplayer_player.angle = p_data.get('angle')
                    mouse_data, mouse_pos = p_data.get('mouse_data', ((0, 0, 0), (0, 0)))
                    # commands = p_data.get('keyboard', ())
                else:
                    # commands = ()
                    mouse_data, mouse_pos = (0, 0, 0), (0, 0)
                self._multiplayer_player.update((),
                                                mouse=self._network_last_data['mouse_data'][0],
                                                mouse_pos=self._network_last_data['mouse_data'][1])
                self._multiplayer_player.draw()

                for addr, player in self._other_multiplayer_players.items():
                    if addr in players_data:
                        p_data = players_data.pop(addr)
                        # value = self._network.str_to_json(value)
                        commands = p_data.get('keyboard', {})
                        player.position = p_data.get('position')
                        player.angle = p_data.get('angle')
                    else:
                        commands = ()

                    player.update(commands)
                    player.draw()

                if players_data:
                    for addr, value in players_data.items():
                        player = SimplePlayer(x=200, y=200, main_player=False,
                                              player_skin=value.get('player_color'),
                                              under_circle_color=1, enemy=True)
                        self._other_multiplayer_players[str(addr)] = player

                        player.position = value.get('position')
                        player.angle = value.get('angle')
                        player.update(value.get('keyboard', {}))
                        player.draw()
                        # print(f'Created player for {addr}')
            # for key, value in data.items():
            #     value = self._network.str_to_json(value)
            #     keyboard = value.get('keyboard', {})
            #     # mouse_data = value.get('mouse_data', ((0, 0, 0), (0, 0)))
            #     position = value.get('position')
            #     angle = value.get('angle')
            #     if key == self._network_address_key:
            #         self._multiplayer_player.update(commands=self._network_last_data['position'],
            #                                         mouse=self._network_last_data['mouse_data'][0],
            #                                         mouse_pos=self._network_last_data['mouse_data'][1])
            #
            #     elif key in self._other_multiplayer_players:
            #         player = self._other_multiplayer_players[key]
            #         if position:
            #             player.position = position
            #         if angle:
            #             player.angle = angle
            #
            #         player.update(keyboard)
            #
            #     else:
            #         player = SimplePlayer(x=200, y=200, main_player=False, player_skin=value.get('player_color'),
            #                               under_circle_color=1, enemy=True)
            #         self._other_multiplayer_players[key] = player
            #         if position:
            #             player.position = position
            #         if angle:
            #             player.angle = angle
            #
            #         player.update(keyboard)

            # TODO: LOGIC for update
            self._multiplayer_cell.draw()
            #
            # self._multiplayer_player.update(commands=self._keyboard.commands,
            #                                 mouse=self._mouse.pressed,
            #                                 mouse_pos=self._mouse.pos)

        for player in self._other_multiplayer_players.values():
            player.draw()

        self._multiplayer_player.draw()

        MUL_ROUND_PAUSE_UI.update()
        MUL_ROUND_PAUSE_UI.draw()

    def MULTIPLAYER_CLIENT_DISCONNECT(self):
        self._other_multiplayer_players.clear()
        self._multiplayer_player = None
        self._multiplayer_cell = None
        self._server_controller = None
        self._network = None
        self._network_address_key = None

        self._g_settings[CURRENT_STAGE] = MAIN_MENU_S
        SERVER_CONTROLLER.stop_server()

    def EXIT(self):
        self._close_game()

    def _close_game(self):
        close_program_pygame()
        sys.exit()
