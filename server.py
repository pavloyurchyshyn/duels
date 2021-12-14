from settings.network_settings.network_settings import *
import socket
from _thread import *
import os
from argparse import ArgumentParser
import logging
import datetime
import json
from player.network_player_object import NetworkPlayerObject
from network.server_game import ServerGame
from network.player_connection_handler import ConnectionHandler
from time import sleep

ROOT_OF_GAME = os.getcwd()
LOGS_FOLDER = os.path.join(ROOT_OF_GAME, 'logs')
START = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")

logging.basicConfig(level=0)
file = logging.FileHandler(filename=f"{LOGS_FOLDER}/{START}_server_logs.txt")

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file.setFormatter(formatter)

LOGGER = logging.getLogger(__file__)
for hdlr in LOGGER.handlers[:]:  # remove all old handlers
    LOGGER.removeHandler(hdlr)

LOGGER.addHandler(file)


class Server:
    def __init__(self):
        self.address = socket.gethostbyname(socket.gethostname())

        arg_parser = ArgumentParser()
        for argument, value in SERVER_ARGUMENTS.items():
            arg_parser.add_argument(argument, default=value[0], help=value[1])

        arguments = arg_parser.parse_args()

        self.player_size = int(arguments.player_size)
        self.game_password = arguments.password
        self.max_number_of_players = int(arguments.players_number)
        self.server_port = int(arguments.port)
        self.time_per_round = int(arguments.time_per_round)
        self.rounds_number = int(arguments.rounds)
        self.game_mode = arguments.game_mode
        self.team_names = arguments.team_names.replace(' ', '').split(',')
        self.admin_access_key = str(arguments.admin) if arguments.admin != 'None' else '_'
        self.admins_list = list(filter(bool, self.admin_access_key.split(',')))
        self.number_of_connected_players = 0

        self.spectators = []

        self.teams = {team: [] for team in self.team_names}  # name of team: players hash

        self.players_connections = {}  # hash: socket connection
        self.player_connected_in_past = set()  # for disconnected players
        self.players_names = {}  # hash: name
        self.players_simple_data = {}
        self.players_objects = {}

        self.ARENA_DATA = {}

        self.SERVER_GAME = ServerGame(max_number_of_rounds=self.max_number_of_players,
                                      teams=self.teams,
                                      time_for_round=self.time_per_round,
                                      cell_data=self.ARENA_DATA,
                                      server=self,
                                      players_connections=self.players_connections,
                                      logger=LOGGER,
                                      players_objects=self.players_objects)

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.address, self.server_port))
        self.socket.listen()
        self.socket_opened = 1
        self.do_not_accept_connections = 0
        self.server_actions = {}

        self.game_thread_id = None

        self.dead_addresses_list = []
        self.ban_list = []  # list of hashes

        self.alive = True

        self.run_game_logic()
        self.run_connection_handling()

    def run_connection_handling(self):
        LOGGER.info(f'Server started {START} {self.address}:{self.server_port}')
        while self.socket_opened:
            if self.do_not_accept_connections:
                sleep(5)
                continue
            try:
                player_connection, (addr, port) = self.socket.accept()
                player_connection = ConnectionHandler(connection=player_connection)
            except Exception as e:
                LOGGER.error(e)
            else:
                player_hash = str(hash(f'{addr} {port}'))

                server_response_data = {CONNECTED: False,
                                        TEAM_SCORES: tuple(self.SERVER_GAME.teams_scores.values()),
                                        CURRENT_ROUND: f"{self.SERVER_GAME.round}/{self.rounds_number}"}

                client_data = self.str_to_json(player_connection.recv(2048).decode())
                network_access_key = client_data.get(NETWORK_ACCESS_KEY)
                if network_access_key in self.players_connections:
                    network_access_key = player_hash

                self.check_for_admin_access_key(network_access_key, player_hash)

                if network_access_key in self.ban_list:
                    server_response_data[SERVER_MESSAGE] = 'You Banned.'
                    player_connection.send(self.json_to_str(server_response_data))
                    player_connection.close()

                LOGGER.info(f'Client credentials: {client_data}')

                # player reconnect
                if network_access_key in self.player_connected_in_past:
                    self.reconnect_player(player_hash=player_hash,
                                          server_response=server_response_data,
                                          network_access_key=network_access_key,
                                          player_data=client_data,
                                          player_connection=player_connection)
                    try:
                        server_response_data[ARENA_DATA] = self.ARENA_DATA
                        player_connection.send(self.json_to_str(server_response_data))
                    except Exception as e:
                        LOGGER.error(f'Failed to connect {network_access_key} {e}')
                        self.disconnect_player(player_hash)

                elif self.number_of_connected_players >= self.max_number_of_players:

                    self.connect_client_as_spectator(server_response_data=server_response_data,
                                                     player_connection=player_connection)
                    player_connection.send(self.json_to_str(server_response_data))
                    server_response_data[ARENA_DATA] = self.ARENA_DATA

                elif client_data[PASSWORD] == self.game_password:
                    self.connect_client_as_player(server_response_data=server_response_data,
                                                  client_data=client_data,
                                                  player_connection=player_connection,
                                                  player_hash=player_hash)
                    server_response_data[ARENA_DATA] = self.ARENA_DATA
                    player_connection.send(self.json_to_str(server_response_data))

                else:
                    server_response_data[SERVER_MESSAGE] = 'Failed to connect, bad password.'
                    LOGGER.info(f'Failed to connect. {anon_host(addr)}. Nickname {client_data[NICKNAME]}')
                    LOGGER.info(f'Bad password! {client_data[PASSWORD]} != {self.game_password}')

                    player_connection.send(self.json_to_str(server_response_data))

    def connect_client_as_player(self, server_response_data, client_data, player_connection, player_hash):
        nickname = self.get_nickname(client_data[NICKNAME], player_hash=player_hash)
        team = self.get_team()
        spawn_position = self.SERVER_GAME.get_spawn_position(team)
        player = NetworkPlayerObject(*spawn_position, team=team,
                                     arena=self.SERVER_GAME.ARENA,
                                     spawn_position=spawn_position)

        if team in self.teams:
            self.teams[team].append(player_hash)
        else:
            self.teams[team] = [player_hash, ]

        self.players_names[player_hash] = nickname
        self.players_connections[player_hash] = player_connection
        self.players_objects[player_hash] = player
        self.players_simple_data[player_hash] = {PLAYER_SKIN: client_data[PLAYER_SKIN],
                                                 NICKNAME: nickname,
                                                 TEAM: team,
                                                 }

        server_response_data[TEAM] = team
        server_response_data[SERVER_MESSAGE] = 'Successfully connected.'
        server_response_data[CONNECTED] = True
        server_response_data[NETWORK_ACCESS_KEY] = player_hash
        server_response_data[POSITION] = player.position

        self.number_of_connected_players += 1
        LOGGER.info(f'Connected. {player_hash}.'
                    f' Player #{self.number_of_connected_players}.'
                    f' Nickname {nickname}.'
                    f' Color: {client_data.get("player_color")}')

    def check_for_admin_access_key(self, player_hash, new_hash):
        if self.admin_access_key == player_hash:
            self.admin_access_key = new_hash
            self.admins_list.append(new_hash)
            if player_hash in self.admins_list:
                self.admins_list.remove(player_hash)
            LOGGER.info(f'Admin connected {new_hash}')

        elif player_hash in self.admins_list:
            self.admins_list.append(new_hash)
            LOGGER.info(f'Admin connected {new_hash}')
            if player_hash in self.admins_list:
                self.admins_list.remove(player_hash)

    def get_team(self) -> str:
        if self.game_mode == CLASSIC_GAME_MODE:
            team = None
            members_number = 999
            for team_, players in self.teams.items():
                if len(players) < members_number:
                    members_number = len(players)
                    team = team_

            return team

        elif self.game_mode == ALL_ARE_ENEMIES_GAME_MODE:
            # TODO add teams logic
            pass

    def connect_client_as_spectator(self, server_response_data, player_connection):
        # TODO automatic connection as spectator
        server_response_data[SERVER_MESSAGE] = 'Server is full. Connect as spectator?.'
        player_connection.send(self.json_to_str(server_response_data))
        player_connection.close()

        LOGGER.info(
            f'Connection limit {self.number_of_connected_players}/{self.max_number_of_players}. Disconnected.')

    def reconnect_player(self, player_hash, server_response, network_access_key, player_data, player_connection):
        LOGGER.info(f'Player {player_hash} is reconnecting.')
        if DELETE_PLAYER in self.server_actions:
            self.server_actions[DELETE_PLAYER].append(network_access_key)
        else:
            self.server_actions[DELETE_PLAYER] = [network_access_key, ]

        nickname = self.get_nickname(player_data[NICKNAME])
        player: NetworkPlayerObject = self.players_objects[network_access_key]

        LOGGER.info(f'Reconnected. {player_hash}.'
                    f' Player #{self.number_of_connected_players}.'
                    f' Nickname {nickname}.'
                    f' Color: {player_data.get("player_color")}')

        server_response[CONNECTED] = True
        server_response[POSITION] = player.position
        server_response[ANGLE] = player.angle
        server_response[HEALTH_POINTS] = player.health_points
        server_response[NETWORK_ACCESS_KEY] = network_access_key
        server_response[SERVER_MESSAGE] = 'Successfully reconnected.'

        self.players_simple_data[network_access_key] = {PLAYER_SKIN: player_data.get(PLAYER_SKIN),
                                                 NICKNAME: nickname,
                                                 TEAM: player.team,
                                                 }

        self.players_connections[network_access_key] = player_connection
        self.player_connected_in_past.remove(network_access_key)
        # self.players_objects[network_access_key] = self.players_objects.pop(network_access_key)

    def run_game_logic(self):
        try:
            self.game_thread_id = start_new_thread(self.SERVER_GAME.run_game, ())
        except Exception as e:
            LOGGER.error(e)
            self.stop_server()

    def get_nickname(self, nickname, player_hash=None) -> str:
        if player_hash in self.players_names:
            return self.players_names[player_hash]

        if nickname in self.players_names:
            same_nick_count = sum(
                [1 for nick in self.players_names if nick == nickname or nick.startswith(f'{nickname}(')])
            return f'{nickname}({same_nick_count})'
        else:
            return nickname

    def stop_server(self):
        self.alive = False
        LOGGER.info('Stopping server')
        LOGGER.info('Disconnecting all players')
        self.disconnect_all_players('Server stopped.')
        try:
            self.socket.close()
            self.socket_opened = 0
            self.stop_game_processor()

        except Exception as e:
            LOGGER.error(f'Failed to stop server. {e}')

    def disconnect_all_players(self, msg_to_players='All players disconnected'):
        data_to_players = self.json_to_str({DISCONNECT: True, SERVER_MESSAGE: msg_to_players})
        for player_hash in self.players_connections.copy():
            try:
                self.players_connections[player_hash].send(data_to_players)
            except Exception as e:
                LOGGER.exception(f'Failed to send data to {player_hash} before disconnect.\n\n{e}')

            try:
                self.disconnect_player(player_hash)
            except Exception as e:
                LOGGER.exception(f'Error while disconnecting {player_hash}: \n\n{e}')

    def disconnect_player(self, player_hash, ban_player=False):
        LOGGER.info(f'Disconnecting player {player_hash}.')
        try:
            self.player_connected_in_past.add(player_hash)
            self.players_connections.pop(player_hash).close()
        except Exception as e:
            LOGGER.error(f"Failed to disconnect {player_hash}: \n\t{e}")
        else:
            LOGGER.info(f'Player {player_hash} disconnected successfully.')

        self.number_of_connected_players -= 1

        if ban_player:
            self.ban_list.append(player_hash)

    def stop_game_processor(self):
        if self.game_thread_id:
            # try:
            #     os.kill(self.game_thread_id, signal.SIGKILL)
            # except Exception as e:
            #     LOGGER.error(e)
            self.game_thread_id = None

    @staticmethod
    def str_to_json(string):
        if not string:
            return {}
        try:
            return json.loads(string)
        except Exception as e:
            LOGGER.error(f"String to json ->{string}<-: \n\t{e}")
            raise Exception(e)

    @staticmethod
    def json_to_str(json_):
        return json.dumps(json_).encode()

    @property
    def all_players_connected(self):
        return self.number_of_connected_players == self.max_number_of_players

    def __del__(self):
        self.stop_server()
        LOGGER.info('Server closed')


if __name__ == '__main__':
    try:
        Server()
    except Exception as e:
        LOGGER.critical(e)
        print(e)
        raise Exception(e)
