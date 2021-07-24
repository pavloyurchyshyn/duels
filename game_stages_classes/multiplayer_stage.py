from network.network import Network

from player_and_spells.player.commands_player import Player
from player_and_spells.player.simple_player import SimplePlayer

from common_things.global_messager import GLOBAL_MESSAGER
from common_things.loggers import LOGGER
from common_things.global_keyboard import GLOBAL_KEYBOARD
from common_things.global_mouse import GLOBAL_MOUSE
from common_things.global_clock import ROUND_CLOCK

from network.server_controller import SERVER_CONTROLLER

from settings.screen_size import X_SCALE, Y_SCALE, GAME_SCALE
from settings.network_settings import CHANGE_CONNECTION, DELETE_PLAYERS, SERVER_ACTION, DELETE_PLAYER, PLAYERS_DATA, SERVER_TIME
from settings.global_parameters import GLOBAL_SETTINGS, pause_step, pause_available
from settings.game_stages import CURRENT_STAGE, MAIN_MENU_S, MAIN_MENU_SETTINGS_S, \
    START_ROUND_S, ROUND_PAUSE_S, ROUND_S, \
    MULTIPLAYER_MENU_S, MULTIPLAYER_CLIENT_DISCONNECT_S, \
    MULTIPLAYER_CLIENT_ROUND_PAUSE_S, MULTIPLAYER_CLIENT_ROUND_S, \
    MULTIPLAYER_CLIENT_S, MULTIPLAYER_HOST_S, HOST_SERVER, \
    EXIT_S, MULTIPLAYER_CLIENT_CONNECT_ROUND_S

from UI.UI_menus.multiplayer import MULTIPLAYER_UI
from world_arena.base.arena_cell import ArenaCell


class MultiplayerStage:
    def __init__(self):
        self._server_controller = None
        self._network: Network = None
        self._network_address_key = None
        self._multiplayer_cell = None
        self._multiplayer_player: Player = None

        self._keyboard = GLOBAL_KEYBOARD
        self._mouse = GLOBAL_MOUSE

        self._other_multiplayer_players: dict = {}
        self._network_last_data = {}
        self._static_client_data = {}
        self._global_messager = GLOBAL_MESSAGER
        self._g_settings = GLOBAL_SETTINGS

    def UPDATE(self, pause=False):
        data_to_send = {
            'keyboard': tuple(self._keyboard.commands),
            'mouse_data': self._mouse.network_data,
            'position': self._multiplayer_player.position,
            'angle': self._multiplayer_player.angle
        }
        data_to_send.update(self._static_client_data)

        # LOGGER.info(f'Player_info: {data_to_send}')
        try:
            if pause:
                data = self._network.update(data=self._network_last_data.copy())
            else:
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

    def MULTIPLAYER_CLIENT_DISCONNECT(self):
        self._other_multiplayer_players.clear()
        self._multiplayer_player = None
        self._multiplayer_cell = None
        self._server_controller = None
        self._network = None
        self._network_address_key = None

        self._g_settings[CURRENT_STAGE] = MAIN_MENU_S
        SERVER_CONTROLLER.stop_server()

