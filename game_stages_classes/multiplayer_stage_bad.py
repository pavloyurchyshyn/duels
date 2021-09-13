from network.network import Network
from network.server_controller import SERVER_CONTROLLER

from player_and_spells.player.commands_player import Player
from player_and_spells.player.simple_player import SimplePlayer

from common_things.global_messager import GLOBAL_MESSAGER
from common_things.loggers import LOGGER
from common_things.global_keyboard import GLOBAL_KEYBOARD
from common_things.global_mouse import GLOBAL_MOUSE
from common_things.global_clock import ROUND_CLOCK

from settings.screen_size import X_SCALE, Y_SCALE, GAME_SCALE, HALF_SCREEN_W, HALF_SCREEN_H
from settings.network_settings.network_settings import DELETE_ALL_PLAYERS, SERVER_ACTION, DELETE_PLAYER, PLAYERS_DATA, \
    SERVER_TIME, DAMAGED
from settings.global_parameters import GLOBAL_SETTINGS, pause_step, pause_available
from settings.game_stages_constants import CURRENT_STAGE, MAIN_MENU_STAGE, \
    MULTIPLAYER_MENU_STAGE, MULTIPLAYER_CLIENT_DISCONNECT_STAGE, \
    MULTIPLAYER_CLIENT_ROUND_PAUSE_STAGE, MULTIPLAYER_CLIENT_ROUND_STAGE
from settings.window_settings import MAIN_SCREEN

from UI.UI_menus.multiplayer import MULTIPLAYER_UI
from world_arena.base.arena_cell import ArenaCellObject
from UI.UI_base.text_UI import Text
from UI.UI_base.messages_UI import Messager


class MultiplayerStage:
    def __init__(self):
        self._server_controller = None
        self._network: Network = None
        self._network_access_key = None
        self._multiplayer_cell = None
        self._multiplayer_player: Player = None

        self._keyboard = GLOBAL_KEYBOARD
        self._mouse = GLOBAL_MOUSE

        self._other_multiplayer_players: dict = {}
        self._network_last_data = {}
        self._static_client_data = {}
        self._global_messager = GLOBAL_MESSAGER
        self._g_settings = GLOBAL_SETTINGS

        self._team_scores_Text = Text('0:0', MAIN_SCREEN, x=HALF_SCREEN_W, y=10 * Y_SCALE, font_size=50 * GAME_SCALE)
        self._current_round_Text = Text('0/0 ROUND', MAIN_SCREEN, x=HALF_SCREEN_W // 2, y=10 * Y_SCALE,
                                        font_size=50 * GAME_SCALE)

        self._round_timer_Text = Text('00:00', MAIN_SCREEN,
                                      x=int(HALF_SCREEN_W * 1.5), y=10 * Y_SCALE,
                                      font_size=50 * GAME_SCALE)

        self._waiting_Text = Text('Waiting for players', MAIN_SCREEN, x=HALF_SCREEN_W, y=100 * Y_SCALE,
                                  font_size=50 * GAME_SCALE)
        self._team_scores = [0, 0]
        self._current_round = '0/0'

        self.winner_message = Messager(x=HALF_SCREEN_W, y=HALF_SCREEN_H, draw_border=False,
                                       draw_surface_every_time=False, message_time=5, background_color=(0, 0, 0, 0))
        self.dead_connections = set()

    def MULTIPLAYER_CLIENT_CONNECT(self):
        self._network = Network()
        ressponse = self._network.connect()

        if self._network.connected:
            LOGGER.info(f'Successfully connected')
            LOGGER.info(f'Server response: {ressponse}')
            self._global_messager.add_message(ressponse.get('server_msg'))
            self._network_access_key = str(ressponse.get('network_address_key'))
            self.dead_connections.update(ressponse.get('dead_addr_list', ()))
            if 'teams_scores' in ressponse:
                self.update_score(ressponse['teams_scores'])

            if 'current_round' in ressponse:
                self.update_round(ressponse['current_round'])

            self._g_settings[CURRENT_STAGE] = MULTIPLAYER_CLIENT_ROUND_STAGE
            data = {}
            self._multiplayer_cell = ArenaCellObject(data, draw_grid=True)

            x, y = ressponse.get('position', (100, 100))
            self._multiplayer_player = Player(x=int(x * X_SCALE), y=int(y * Y_SCALE))
            self._multiplayer_player.position = ressponse.get('position')
            self._multiplayer_player.angle = ressponse.get('angle')
            self._multiplayer_player.hp = ressponse.get('hp')
            self._multiplayer_player.update({}, (0, 0, 0), (0, 0))

            self._static_client_data['player_color'] = self._multiplayer_player.color

            self._other_multiplayer_players.clear()
        else:
            MULTIPLAYER_UI.network_messager.add_message(ressponse.get('server_msg'))
            self._g_settings[CURRENT_STAGE] = MULTIPLAYER_MENU_STAGE

    def UPDATE(self, pause=False):
        data_to_send = {
            'keyboard': tuple(self._keyboard.commands),
            'mouse_data': self._mouse.network_data,
            'position': self._multiplayer_player.position,
            'angle': self._multiplayer_player.angle
        }

        data_to_send.update(self._static_client_data)

        try:
            if pause:
                data = self._network.update(data=self._network_last_data.copy())
            else:
                data = self._network.update(data=data_to_send)
                self._network_last_data = data_to_send.copy()
            data_to_send.clear()
        except Exception as e:
            LOGGER.error(f"Failed to receive server response with error:\n\t {e}")
            self._g_settings[CURRENT_STAGE] = MULTIPLAYER_CLIENT_DISCONNECT_STAGE
            self._global_messager.add_message('Server connection lost')

        else:
            if 'round_winner' in data:
                self.winner_message.add_message(data['round_winner'])

            if data.get('disconnect', False):
                self._g_settings[CURRENT_STAGE] = MULTIPLAYER_CLIENT_DISCONNECT_STAGE

            self.update_score(data.get('teams_scores'))

            self.update_round(data.get('current_round'))

            ROUND_CLOCK.set_time(*data.pop(SERVER_TIME))
            self._round_timer_Text.change_text(ROUND_CLOCK.timer_format)

            if SERVER_ACTION in data:
                server_action = data.pop(SERVER_ACTION)
                if DELETE_ALL_PLAYERS in server_action and server_action.pop(DELETE_ALL_PLAYERS):
                    self._other_multiplayer_players.clear()

                if DELETE_PLAYER in server_action:
                    for player_addr in server_action[DELETE_PLAYER]:
                        self.dead_connections.add(player_addr)
                        if player_addr in self._other_multiplayer_players:
                            self._other_multiplayer_players.pop(player_addr)

                        if player_addr in data[PLAYERS_DATA]:
                            data[PLAYERS_DATA].pop(player_addr)

            # TODO: LOGIC for update
            self._multiplayer_cell.draw()
            if PLAYERS_DATA in data and data[PLAYERS_DATA]:
                players_data = data[PLAYERS_DATA]
                if self._network_access_key in players_data:
                    p_data = players_data.pop(self._network_access_key)
                    if p_data.get('revise', False):
                        self._multiplayer_player.revise()

                    self._multiplayer_player.position = p_data.get('position')
                    self._multiplayer_player.angle = p_data.get('angle')
                    self._multiplayer_player.damage(p_data.get(DAMAGED))
                    self._multiplayer_player.hp = p_data.get('hp')

                    mouse_data, mouse_pos = p_data.get('mouse_data', ((0, 0, 0), (0, 0)))
                    commands = p_data.get('keyboard', ())
                else:
                    commands = ()
                    mouse_data, mouse_pos = (0, 0, 0), (0, 0)

                self._multiplayer_player.update((), mouse=mouse_data, mouse_pos=GLOBAL_MOUSE.pos)
                self._multiplayer_player.draw()

                for addr, player in self._other_multiplayer_players.copy().items():
                    if addr in players_data:
                        p_data = players_data.pop(addr)
                        commands = p_data.get('keyboard', {})
                        player.position = p_data.get('position')
                        player.angle = p_data.get('angle')
                        player.damage(p_data.get(DAMAGED))
                        player.hp = p_data.get('hp')

                    else:
                        commands = ()

                    player.update(commands)
                    player.draw()

                if players_data:
                    for addr, value in players_data.items():
                        if addr in self.dead_connections:
                            continue

                        player = SimplePlayer(x=200, y=200, main_player=False,
                                              player_skin=value.get('player_color'),
                                              under_circle_color=1, enemy=True)
                        self._other_multiplayer_players[addr] = player
                        print(f'Player {addr} created')
                        player.position = value.get('position')
                        player.angle = value.get('angle')

                        if value.get('revise', False):
                            player.revise()

                        player.hp = value.get('hp')

                        player.update(value.get('keyboard', {}))
                        player.draw()
                del players_data
            if data.get('waiting_players', False):
                self._waiting_Text.draw()

        if GLOBAL_KEYBOARD.ESC and pause_available():
            pause_step()
            self._g_settings[CURRENT_STAGE] = MULTIPLAYER_CLIENT_ROUND_PAUSE_STAGE
            self._network_last_data['keyboard'] = {}

        self.winner_message.update()
        self._round_timer_Text.update()
        self._team_scores_Text.draw()
        self._current_round_Text.draw()
        self._round_timer_Text.draw()
        self.winner_message.draw()

    def MULTIPLAYER_CLIENT_DISCONNECT(self):
        self._other_multiplayer_players.clear()
        self._multiplayer_player = None
        self._multiplayer_cell = None
        self._server_controller = None
        self._network = None
        self._network_access_key = None

        self._g_settings[CURRENT_STAGE] = MAIN_MENU_STAGE
        SERVER_CONTROLLER.stop_server()

    def update_score(self, scores: tuple):
        if scores and scores != self._team_scores:
            self._team_scores = scores
            self._team_scores_Text.change_text(':'.join(map(str, scores)))

    def update_round(self, round):
        if round and self._current_round != round:
            self._current_round = round
            self._current_round_Text.change_text(f"{round} ROUND")


GLOBAL_MUL_STAGE = MultiplayerStage()
