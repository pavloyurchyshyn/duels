from network.network import Network
from network.server_controller import SERVER_CONTROLLER
from common_things.camera import GLOBAL_CAMERA
# from player_and_spells.player.commands_player import Player
from player_and_spells.player.simple_player import SimplePlayer

from common_things.global_messager import GLOBAL_MESSAGER
from common_things.loggers import LOGGER
from common_things.global_keyboard import GLOBAL_KEYBOARD
from common_things.global_mouse import GLOBAL_MOUSE
from common_things.global_clock import ROUND_CLOCK

# from settings.screen_size import X_SCALE, Y_SCALE, GAME_SCALE
X_SCALE, Y_SCALE, GAME_SCALE = 1, 1, 1

from settings.screen_size import HALF_SCREEN_W, HALF_SCREEN_H
from settings.global_parameters import GLOBAL_SETTINGS, pause_step, pause_available, set_multiplayer_menu_stage, \
    set_multiplayers_round_stage, set_multiplayers_disconnect_stage, set_multiplayers_round_pause_stage, \
    set_main_menu_stage
from settings.window_settings import MAIN_SCREEN
from settings.network_settings.network_constants import *

from UI.UI_menus.multiplayer import MULTIPLAYER_UI
from world_arena.base.arena_cell import ArenaCell
from UI.UI_base.text_UI import Text
from UI.UI_base.messages_UI import Messager


class MultiplayerStage:
    def __init__(self):
        self._server_controller = None
        self._network: Network = None
        self._network_access_key = None
        self._multiplayer_cell: ArenaCell = None
        self._this_multiplayer_player: SimplePlayer = None

        self._keyboard = GLOBAL_KEYBOARD
        self._mouse = GLOBAL_MOUSE

        self._other_multiplayer_players_objects: dict = {}
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
        self._current_round_str = '0/0'

        self.winner_message = Messager(x=HALF_SCREEN_W, y=HALF_SCREEN_H, draw_border=False,
                                       draw_surface_every_time=False, message_time=5,
                                       background_color=(0, 0, 0, 0))

    def MULTIPLAYER_CLIENT_CONNECT(self):
        self._network = Network()
        server_response = self._network.connect()
        if self._network.connected:
            LOGGER.info(f'Successfully connected')
            LOGGER.info(f'Server response: {server_response}')
            self._global_messager.add_message(server_response.get(SERVER_MESSAGE))
            self._network_access_key = server_response.get(NETWORK_ACCESS_KEY)
            if TEAM_SCORES in server_response:
                self.update_score(server_response[TEAM_SCORES])

            if CURRENT_ROUND in server_response:
                self.update_round(server_response[CURRENT_ROUND])

            self._multiplayer_cell = ArenaCell(server_response[ARENA_DATA], draw_grid=True)

            x, y = server_response.get(POSITION, (100, 100))
            self._this_multiplayer_player = SimplePlayer(x=int(x * X_SCALE), y=int(y * Y_SCALE), follow_mouse=True)
            self._this_multiplayer_player.angle = server_response.get(ANGLE)
            self._this_multiplayer_player.health_points = server_response.get(HEALTH_POINTS)
            self._this_multiplayer_player.update()

            self._static_client_data[PLAYER_SKIN] = self._this_multiplayer_player.color

            self._other_multiplayer_players_objects.clear()

            set_multiplayers_round_stage()

        else:
            MULTIPLAYER_UI.network_messager.add_message(server_response.get(SERVER_MESSAGE))
            set_multiplayer_menu_stage()

    def UPDATE(self, pause=False):
        data_to_send = {
            'keyboard': tuple(self._keyboard.commands),
            'mouse_data': self._mouse.network_data,
            POSITION: self._this_multiplayer_player.position,
            ANGLE: self._this_multiplayer_player.angle
        }

        data_to_send.update(self._static_client_data)

        try:
            if pause:
                data_from_server = self._network.update(data=self._network_last_data.copy())
            else:
                data_from_server = self._network.update(data=data_to_send)
                self._network_last_data = data_to_send.copy()

        except Exception as e:
            LOGGER.error(f"Failed to receive server response with error:\n\t {e}")
            set_multiplayers_disconnect_stage()
            self._global_messager.add_message('Server connection lost')

        else:
            if ROUND_WINNER in data_from_server:
                self.winner_message.add_message(data_from_server[ROUND_WINNER])

            if data_from_server.get('disconnect', False):
                set_multiplayers_disconnect_stage()

            self.update_score(data_from_server.get(TEAM_SCORES))
            self.update_round(data_from_server.get(CURRENT_ROUND))
            ROUND_CLOCK.set_time(*data_from_server.get(SERVER_TIME, (-999, -999)))
            self._round_timer_Text.change_text(ROUND_CLOCK.timer_format)

            self._multiplayer_cell.draw()
            self.add_new_objects(data_from_server)
            self.delete_objects(data_from_server)
            self._multiplayer_cell.update()

            self.process_server_action(data_from_server=data_from_server)

            if PLAYERS_DATA in data_from_server and data_from_server[PLAYERS_DATA]:
                players_data = data_from_server[PLAYERS_DATA]

                self.update_this_player(players_data)
                self.update_and_draw_other_players(players_data=players_data)
                self.create_new_players(players_data=players_data)

            if data_from_server.get(WAITING_PLAYERS, False):
                self._waiting_Text.draw()

            if data_from_server.get(DISCONNECT, 0):
                self._global_messager.add_message(data_from_server.get(SERVER_MESSAGE, ''))
                set_multiplayers_disconnect_stage()

        self._this_multiplayer_player.draw()

        if GLOBAL_KEYBOARD.ESC and pause_available():
            pause_step()
            set_multiplayers_round_pause_stage()
            self._network_last_data['keyboard'] = {}

        self.winner_message.update()
        self._round_timer_Text.update()

        self._team_scores_Text.draw()
        self._current_round_Text.draw()
        self._round_timer_Text.draw()
        self.winner_message.draw()

    def process_server_action(self, data_from_server):
        if SERVER_ACTION in data_from_server:
            server_action = data_from_server[SERVER_ACTION]
            if server_action.get(DELETE_ALL_PLAYERS, False):
                self._other_multiplayer_players_objects.clear()

            if DELETE_PLAYER in server_action:
                for player_hash_to_delete in server_action[DELETE_PLAYER]:
                    if player_hash_to_delete in self._other_multiplayer_players_objects:
                        self._other_multiplayer_players_objects.pop(player_hash_to_delete)

                    if player_hash_to_delete in data_from_server[PLAYERS_DATA]:
                        data_from_server[PLAYERS_DATA].pop(player_hash_to_delete)

    def add_new_objects(self, data_from_server):
        if ADD_OBJECTS in data_from_server:
            for object_data in data_from_server[ADD_OBJECTS]:
                self._multiplayer_cell.add_object(object_data, from_server=1)

    def delete_objects(self, data_from_server):
        if DELETE_OBJECTS in data_from_server:
            for key in data_from_server[DELETE_OBJECTS]:
                self._multiplayer_cell.delete_object_by_key(obj_key=key)

    def update_this_player(self, players_data):
        if self._network_access_key in players_data:
            player_data = players_data.pop(self._network_access_key)
            if player_data.get(REVISE, False):
                self._this_multiplayer_player.revise()

            self._this_multiplayer_player.angle = player_data.get(ANGLE)
            self._this_multiplayer_player.damage(player_data.get(DAMAGED))
            self._this_multiplayer_player.health_points = player_data.get(HEALTH_POINTS)
            self._this_multiplayer_player.position = player_data[POSITION]
            GLOBAL_CAMERA.update(player_pos=player_data[POSITION])

            commands = player_data.get('keyboard', ())

        else:
            commands = ()

        self._this_multiplayer_player.update(commands)

    def update_and_draw_other_players(self, players_data):
        for player_hash, player in self._other_multiplayer_players_objects.items():
            if player_hash in players_data:
                player_data = players_data.pop(player_hash)
                commands = player_data.get('keyboard', {})
                player.angle = player_data.get(ANGLE)
                player.damage(player_data.get(DAMAGED))
                player.health_points = player_data.get(HEALTH_POINTS)
                player.update(commands)
                player.position = player_data.get(POSITION)
                if player_data.get(REVISE, False):
                    player.revise()
            else:
                commands = ()
                player.update(commands)

            player.draw()

    def create_new_players(self, players_data):
        if players_data:
            for player_hash, player_data in players_data.items():
                player = SimplePlayer(*player_data.get(POSITION, (100, 100)),
                                      main_player=False,
                                      player_skin=player_data.get(PLAYER_SKIN),
                                      under_circle_color=1, enemy=True)

                self._other_multiplayer_players_objects[player_hash] = player

                player.angle = player_data.get(ANGLE)
                if player_data.get(REVISE, False):
                    player.revise()
                player.health_points = player_data.get(HEALTH_POINTS)

                player.update(player_data.get('keyboard', {}))
                player.draw()

    def update_score(self, scores: tuple):
        if scores and scores != self._team_scores:
            self._team_scores = scores
            self._team_scores_Text.change_text(':'.join(map(str, scores)))

    def update_round(self, round):
        if round and self._current_round_str != round:
            self._current_round_str = round
            self._current_round_Text.change_text(f"{round} ROUND")

    def MULTIPLAYER_CLIENT_DISCONNECT(self):
        SERVER_CONTROLLER.stop_server()

        if self._network:
            self._network.send(data={STOP_SERVER: True})
        self._other_multiplayer_players_objects.clear()
        self._this_multiplayer_player = None
        self._multiplayer_cell = None
        self._server_controller = None
        self._network = None
        self._network_access_key = None

        set_main_menu_stage()


GLOBAL_MUL_STAGE = MultiplayerStage()
