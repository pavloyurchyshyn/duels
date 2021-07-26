import socket

from _thread import *
import sys
import os
import re
import signal
import logging
import datetime
import json
from random import choice as random_choice
from time import time, sleep
from argparse import ArgumentParser
from settings.network_settings import DEFAULT_PORT, anon_host, PASSWORD, PORT, NICKNAME, TEAM_SCORES, DAMAGED, DEAD, \
    DELETE_PLAYERS, SERVER_ACTION, DELETE_PLAYER, PLAYERS_DATA, SERVER_TIME, DEFAULT_TIME_PER_ROUND, CURRENT_ROUND, \
    ROUND_WINNER
from settings.players_settings.player_settings import PLAYER_SIZE
from common_things.global_clock import Clock
from world_arena.base.arena_cell_obj import ArenaCell
from player_and_spells.player.player_object import PlayerObject

from common_things.global_clock import ROUND_CLOCK

DISCONNECT_TIMEOUT = 60

ROOT_OF_GAME = os.getcwd()
LOGS_FOLDER = os.path.join(ROOT_OF_GAME, 'logs')
START = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")

logging.basicConfig(filename=os.path.join(LOGS_FOLDER, "{}_server_logs.txt".format(START)), level=0)
LOGGER = logging.getLogger(__name__)


class Server:
    ERRORS_TRIES = 5
    TIMEOUT = 5

    ARGUMENTS = {
        '--port': [DEFAULT_PORT, 'Server Port'],
        '--pnum': ['2', 'Number of players'],
        '--password': ['.', 'Lobby password'],
        '--rounds': [10, 'Needed round to win'],
        '--time_per_round': [DEFAULT_TIME_PER_ROUND, 'Time for round in minutes']
    }

    def __init__(self):
        self.address = socket.gethostbyname(socket.gethostname())
        self.port = DEFAULT_PORT

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.players_max_number = 2
        self.players_connected = 0
        self.rounds = 10
        self.time_per_round = DEFAULT_TIME_PER_ROUND
        self.password = '.'

        self.parse_args()

        self.socket.bind((self.address, self.port))
        self.socket.listen()
        self.socket_opened = 1

        self.players_connections = {}  # connections dict of sockets
        self.players_names = {}  # just names
        self.players_objects = {}  # game objects
        self.players_data = {}  # received data from player
        self.players_common_data = {}  # players nicknames, colors, etc.

        # TODO make teams generic
        self.teams = {
            'red': [],
            'blue': [],
            'spectator': [],
        }

        self.player_connected_in_past = {}  # for disconnected players

        self.cell_data = {}
        self.server_actions = {}

        self.SERVER_GAME = ServerGame(self.players_connections, self, cell_data=self.cell_data,
                                      players_objects=self.players_objects, teams=self.teams,
                                      rounds=self.rounds, time_per_round=self.time_per_round)

        self.game_thread_id = None
        self.run_game()
        self.run()

    def parse_args(self):
        arg_parser = ArgumentParser()
        for argument, value in Server.ARGUMENTS.items():
            arg_parser.add_argument(argument, default=value[0], help=value[1])

        arguments = arg_parser.parse_args()
        self.password = arguments.password
        self.players_max_number = int(arguments.pnum)
        self.port = int(arguments.port)
        self.time_per_round = int(arguments.time_per_round)
        self.rounds = int(arguments.rounds)

    def run(self):
        LOGGER.info(f'Server started {START} {self.address}:{self.port}')

        while self.socket_opened:
            # self.server_actions.clear()
            conn, addr = self.socket.accept()
            str_addr = str(addr)
            LOGGER.info(f'Accepted: {anon_host(addr)}')

            server_response_data = {'connected': False,
                                    'teams_scores': tuple(self.SERVER_GAME.teams_scores.values()),
                                    CURRENT_ROUND: f"{self.SERVER_GAME.round}/{self.rounds}"}
            recv = conn.recv(2048).decode()

            credentials = self.str_to_json(recv)
            network_acc_k = credentials.get('network_address_key')
            LOGGER.info(f'Client credentials: {credentials}')
            LOGGER.info(
                f"Network_address_key {network_acc_k} in {set(self.player_connected_in_past.keys())} is {credentials.get('network_address_key') in set(self.player_connected_in_past.keys())}")

            if network_acc_k in self.player_connected_in_past:
                server_response_data['connected'] = True

                player: PlayerObject = self.players_objects[network_acc_k]

                server_response_data['position'] = player.position
                server_response_data['angle'] = player.angle
                server_response_data['hp'] = player.hp

                self.server_actions[DELETE_PLAYER] = network_acc_k
                server_response_data['network_address_key'] = str_addr
                server_response_data['server_msg'] = 'Successfully reconnected.'

                nickname = self.get_nickname(credentials[NICKNAME])

                LOGGER.info(f'Reconnected. {anon_host(addr)}.'
                            f' Player #{self.players_connected}.'
                            f' Nickname {nickname}.'
                            f' Color: {credentials.get("player_color")}')

                self.players_common_data[str_addr] = {'player_color': credentials.get("player_color"),
                                                      NICKNAME: nickname,
                                                      'team': player.team
                                                      }
                self.players_connections[str_addr] = conn

                self.player_connected_in_past.pop(network_acc_k)
                self.players_objects[str_addr] = self.players_objects.pop(network_acc_k)

                conn.send(self.json_to_str(server_response_data))

            elif self.players_connected >= self.players_max_number:  # ------->
                server_response_data['server_msg'] = "Failed to connect. Server is full."
                conn.send(self.json_to_str(server_response_data))
                conn.close()
                LOGGER.info(
                    f'Connection limit {self.players_connected}/{self.players_max_number}. Disconnected {anon_host(addr)}')
            else:
                LOGGER.info(f'Credentials: {credentials}')

                if credentials[PASSWORD] == self.password:
                    LOGGER.info(f'Password is good! {credentials[PASSWORD]} == {self.password}')
                    self.players_connected += 1
                    nickname = self.get_nickname(credentials[NICKNAME])

                    self.players_names[nickname] = addr
                    server_response_data['connected'] = True
                    server_response_data['position'] = (500, 500)
                    server_response_data['network_address_key'] = str(addr)
                    server_response_data['server_msg'] = 'Successfully connected.'
                    conn.send(self.json_to_str(server_response_data))

                    team = 'red' if len(self.teams['red']) < len(self.teams['blue']) else 'blue'
                    server_response_data['team'] = team
                    self.teams[team].append(str(addr))

                    self.players_connections[str(addr)] = conn
                    self.players_objects[str(addr)] = PlayerObject(*self.SERVER_GAME.get_spawn_pos(team), team=team)
                    self.players_data[str(addr)] = credentials
                    self.players_common_data[str(addr)] = {'player_color': credentials.get("player_color"),
                                                           NICKNAME: nickname,
                                                           'team': team,
                                                           }

                    LOGGER.info(f'Connected. {anon_host(addr)}.'
                                f' Player #{self.players_connected}.'
                                f' Nickname {nickname}.'
                                f' Color: {credentials.get("player_color")}')
                else:
                    server_response_data['server_msg'] = 'Failed to connect, bad password.'

                    conn.send(self.json_to_str(server_response_data))

                    LOGGER.info(f'Failed to connect. {anon_host(addr)}. Nickname {credentials[NICKNAME]}')
                    LOGGER.info(f'Bad password! {credentials[PASSWORD]} != {self.password}')

    @staticmethod
    def str_to_json(string):
        try:
            return json.loads(string)
        except Exception as e:
            LOGGER.error(f"String to json {string}: \n\t{e}")
            raise Exception(e)

    @staticmethod
    def json_to_str(json_):
        return json.dumps(json_).encode()

    def disconnect_player(self, addr, del_player=True):
        LOGGER.info(f'Disconnecting player {addr}')
        try:
            try:
                self.send(*self.players_connections[addr], data=self.json_to_str({'disconnect': True}))
            except Exception as e:
                LOGGER.error(f"Failed to send disconnect command to client: \n\t {e}")

            self.players_connections[addr].close()
        except Exception as e:
            LOGGER.error(f"Failed to disconnect {addr}: \n\t{e}")
        else:
            LOGGER.info(f'Player {addr} disconnected successfully.')

        if del_player:
            self.player_connected_in_past[addr] = self.players_connections.pop(addr)
            LOGGER.info(f'Player {addr} deleted from {self.players_connections} to {self.player_connected_in_past}.')
            self.players_connected -= 1

        LOGGER.info(f'Players number: {self.players_connected}')

    def get_nickname(self, nickname):
        if nickname in self.players_names:
            same_nick_count = sum(
                [1 for nick in self.players_names if nick == nickname or nick.startswith(f'{nickname}(')])
            return f'{nickname}({same_nick_count})'
        else:
            return nickname

    def disconnect_all_players(self):
        for connect in self.players_connections:
            self.disconnect_player(connect, del_player=True)

    def stop_server(self):
        self.disconnect_all_players()
        try:
            self.socket.close()
            self.socket_opened = 0
            if self.game_thread_id:
                os.kill(self.game_thread_id, signal.SIGKILL)
        except Exception:
            pass

    def __del__(self):
        self.stop_server()
        LOGGER.info('Server closed')

    def finish_game(self):
        # disconnect players
        # kill game server
        pass

    def run_game(self):
        self.game_thread_id = start_new_thread(self.SERVER_GAME.run, ())

    def send(self, addr, sock, data):
        try:
            sock.send(data)
        except Exception as e:
            LOGGER.error(f'Failed to send data to {anon_host(addr)}: \n\t{e}')
            self.disconnect_player(addr)

    @property
    def all_players_connected(self):
        return self.players_connected == self.players_max_number


class ServerGame:
    TICK_RATE = 64

    def __init__(self, players_connections, server,
                 cell_data, players_objects,
                 teams, rounds, time_per_round):
        self.server: Server = server
        self.players_connections: dict = players_connections

        self.teams = teams.copy()  # teams with all players
        self.teams.pop('spectator')

        self.teams_scores = {team: 0 for team in self.teams}

        self.rounds = rounds
        self.round = 0
        self.time_for_round = time_per_round

        self.win_score = rounds // 2 + 1  # needed rounds to win, if 10 rounds -> 6 to win

        self.teams_alive_players = {}

        self.stages = {
            'round': self.ROUND,
            'prepare_to_round': self.PREPARING_TO_ROUND,
            'finish': self.FINISH_GAME,
            'waiting_for_players': self.WAITING_FOR_PLAYERS,
            'round_finished': self.ROUND_FINISHED,
        }
        self.current_stage = 'waiting_for_players'

        self.players_data = {}  # data sent by players
        self.players_data_to_send = {}  # data which sends to players
        self.players_objects = players_objects

        self.clock = ROUND_CLOCK
        self.data_to_send = {}

        self.ARENA = ArenaCell(data=cell_data)

        self.spawn_positions = {
            'red': set((x, y) for x in range(50, 100, 50) for y in range(0, self.ARENA._size, 50)),
            'blue': set((x, y) for x in range(self.ARENA._size - 50, self.ARENA._size, 50) for y in
                        range(0, self.ARENA._size, 50)),
        }
        self.used_spawn_pos = set()

    def run(self):
        LOGGER.info('Sever Game loop started.')
        update_delay = 1 / self.TICK_RATE
        LOGGER.info(f'Tick rate {self.TICK_RATE}. Time per frame: {update_delay}')

        next_update = -1
        while True:
            t = time()
            if t > next_update:
                next_update = t + update_delay
                self.clock.update(update_delay)
                self.stages[self.current_stage]()
            elif next_update - t - 0.05 > 0.01:
                sleep(next_update - t - 0.05)

    def WAITING_FOR_PLAYERS(self):
        self.ARENA.update()
        self.data_to_send.clear()
        for addr, conn in self.players_connections.copy().items():
            try:
                data = conn.recv(2048).decode()
            except Exception as e:
                self.server.disconnect_player(addr)
                # data = b''
                LOGGER.error(f'Failed to get info from {addr}: \n\t{e}')
            else:
                if data:
                    if "}{" in data:
                        data = f"{'{'}{data.split('}{')[-1]}"

                    data = self.server.str_to_json(data)
                    player: PlayerObject = self.players_objects[str(addr)]
                    if player.alive:
                        player.angle = data.get('angle')
                        player_action = player.update(commands=data.get('keyboard'),
                                                      mouse_buttons=data.get('mouse_data')[0],
                                                      mouse_pos=data.get('mouse_data')[1])

                        self.players_data[str(addr)] = {
                            'position': player.position,
                            'angle': player.angle,
                            'player_action': player_action,
                            'hp': player.hp,
                            DAMAGED: player.damaged,
                            DEAD: player.dead,
                        }
                        # if player.dead:
                        #     self.teams_alive_players[player.team].pop(str(addr))

                    else:
                        player.position = player.spawn_position
                        player.hp = player.full_hp
                        player_action = player.update()
                        self.players_data[str(addr)] = {
                            'position': player.position,
                            'angle': player.angle,
                            'player_action': player_action,
                            DAMAGED: player.damaged,
                            'hp': player.hp,
                            DEAD: player.dead,
                            'revise': 1,
                        }

        self.data_to_send[PLAYERS_DATA] = self.players_data
        if self.server.server_actions:
            self.data_to_send[SERVER_ACTION] = self.server.server_actions.copy()
            self.server.server_actions.clear()

        self.data_to_send['waiting_players'] = True
        self.data_to_send[SERVER_TIME] = self.clock()
        self.data_to_send[TEAM_SCORES] = tuple(self.teams_scores.values())
        self.data_to_send[CURRENT_ROUND] = f"{self.round}/{self.rounds}"

        self.send_data_to_players()
        if self.server.all_players_connected:
            self.current_stage = 'prepare_to_round'

    def PREPARING_TO_ROUND(self):
        self.round += 1
        for team, players in self.teams.items():
            self.teams_alive_players[team] = players.copy()

        self.used_spawn_pos.clear()

        for addr, player in self.players_objects.items():
            while 1:
                pos = random_choice(tuple(self.spawn_positions[self.server.players_common_data[addr]['team']]))
                if pos not in self.used_spawn_pos:
                    self.used_spawn_pos.add(pos)
                    player.position = pos
                    player.spawn_position = pos
                    player.hp = player.full_hp
                    break

        self.clock.set_time(-10, 0)

        self.current_stage = 'round'

    def ROUND_PAUSE(self):
        pass

    def ROUND(self):
        self.ARENA.update()
        self.update_players_data(players_disabled=self.clock.time < 0)

        self.data_to_send[PLAYERS_DATA] = self.players_data
        if self.server.server_actions:
            self.data_to_send[SERVER_ACTION] = self.server.server_actions.copy()
            self.server.server_actions.clear()

        self.data_to_send[SERVER_TIME] = self.clock()
        self.data_to_send[TEAM_SCORES] = tuple(self.teams_scores.values())
        self.data_to_send[CURRENT_ROUND] = f"{self.round}/{self.rounds}"

        dead_teams = (team for team, players in self.teams_alive_players.copy().items() if len(players) == 0)
        if dead_teams:
            for team in dead_teams:
                self.teams_alive_players.pop(team)

            if len(self.teams_alive_players) == 1:
                team = tuple(self.teams_alive_players.keys())[0]
                LOGGER.info(f"TEAM {team.upper()} WON")
                self.data_to_send[ROUND_WINNER] = team.upper()
                self.teams_scores[team] += 1
                self.current_stage = 'round_finished'

            elif len(self.teams_alive_players) == 0:
                self.data_to_send[ROUND_WINNER] = 'DRAW'
                LOGGER.info(f"DRAW")
                self.current_stage = 'round_finished'

        self.send_data_to_players()
        self.data_to_send.clear()

    def ROUND_FINISHED(self):
        if self.round != self.rounds:
            self.current_stage = 'prepare_to_round'
        else:
            self.current_stage = 'finish'

    def FINISH_GAME(self):
        # self.server.stop_server()
        raise Exception('Game finished successfully.')

    def game_finished(self):
        self.server.finish_game()

    def update_players_data(self, players_disabled):
        for addr, conn in self.players_connections.copy().items():
            try:
                data = conn.recv(2048).decode()
            except Exception as e:
                self.server.disconnect_player(addr)
                # data = b''
                LOGGER.error(f'Failed to get info from {addr}: \n\t{e}')
            else:
                if data:
                    if "}{" in data:
                        data = f"{'{'}{data.split('}{')[-1]}"

                    data = self.server.str_to_json(data)
                    player: PlayerObject = self.players_objects[str(addr)]

                    if player.alive:
                        player.angle = data.get('angle')
                        commands = () if players_disabled else data.get('keyboard')
                        mouse_data = (0, 0, 0) if players_disabled else data.get('mouse_data')[0]
                        player_action = player.update(commands=commands,
                                                      mouse_buttons=mouse_data,
                                                      mouse_pos=data.get('mouse_data')[1])

                        self.players_data[str(addr)] = {
                            'position': player.position,
                            'angle': player.angle,
                            'player_action': player_action,
                            DAMAGED: player.damaged,
                            DEAD: player.dead,
                            'hp': player.hp,
                        }
                        if player.dead:
                            self.teams_alive_players[player.team].remove(str(addr))

                    else:
                        player_action = player.update()
                        self.players_data[str(addr)] = {
                            'position': player.position,
                            'angle': player.angle,
                            'player_action': player_action,
                            DAMAGED: player.damaged,
                            DEAD: player.dead,
                        }

    def send_data_to_players(self):

        json_data = json.dumps(self.data_to_send).encode()

        for addr, sock in self.players_connections.copy().items():
            try:
                sock.send(json_data)
            except Exception as e:
                self.server.disconnect_player(addr)

        self.data_to_send.clear()

    def get_spawn_pos(self, team):
        while 1:
            pos = random_choice(tuple(self.spawn_positions[team]))
            if pos not in self.used_spawn_pos:
                self.used_spawn_pos.add(pos)
                return pos

    def __del__(self):
        LOGGER.info(f'Game server was closed.')


if __name__ == '__main__':
    try:
        Server()
    except Exception as e:
        LOGGER.critical(e)
        print(e)
        raise Exception(e)
