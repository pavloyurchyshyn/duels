import socket

from _thread import *
import sys
import os
import re
import signal
import logging
import datetime
import json
from time import time, sleep
from argparse import ArgumentParser
from settings.network_settings import DEFAULT_PORT, anon_host, PASSWORD, PORT, NICKNAME, \
    CHANGE_CONNECTION, DELETE_PLAYERS, SERVER_ACTION, DELETE_PLAYER, PLAYERS_DATA, SERVER_TIME
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
    }

    def __init__(self):
        self.address = socket.gethostbyname(socket.gethostname())
        self.port = DEFAULT_PORT

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.players_number = 2
        self.players_connected = 0

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

        self.player_connected_in_past = {}  # for disconnected players

        self.cell_data = {}
        self.server_actions = {}

        self.SERVER_GAME = ServerGame(self.players_connections, self, cell_data=self.cell_data,
                                      players_objects=self.players_objects)

        self.game_thread_id = None
        self.run_game()
        self.run()

    def parse_args(self):
        arg_parser = ArgumentParser()
        for argument, value in Server.ARGUMENTS.items():
            arg_parser.add_argument(argument, default=value[0], help=value[1])

        arguments = arg_parser.parse_args()
        self.password = arguments.password
        self.players_number = int(arguments.pnum)
        self.port = int(arguments.port)
        pass

    def run(self):
        LOGGER.info(f'Server started {START} {self.address}:{self.port}')

        while self.socket_opened:
            # self.server_actions.clear()
            conn, addr = self.socket.accept()
            str_addr = str(addr)
            LOGGER.info(f'Accepted: {anon_host(addr)}')

            server_response_data = {'connected': False}
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
                #  server_response_data['position'] = self.player_connected_in_past['position']
                server_response_data['server_msg'] = 'Successfully reconnected.'

                nickname = self.get_nickname(credentials[NICKNAME])

                LOGGER.info(f'Reconnected. {anon_host(addr)}.'
                            f' Player #{self.players_connected}.'
                            f' Nickname {nickname}.'
                            f' Color: {credentials.get("player_color")}')
                self.players_common_data[str_addr] = {'player_color': credentials.get("player_color"),
                                                      NICKNAME: nickname
                                                      }
                self.players_connections[str_addr] = conn

                self.player_connected_in_past.pop(network_acc_k)
                self.players_objects[str_addr] = self.players_objects.pop(network_acc_k)

                conn.send(self.json_to_str(server_response_data))

            elif self.players_connected >= self.players_number:  # ------->
                server_response_data['server_msg'] = "Failed to connect. Server is full."
                conn.send(self.json_to_str(server_response_data))
                conn.close()
                LOGGER.info(
                    f'Connection limit {self.players_connected}/{self.players_number}. Disconnected {anon_host(addr)}')
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

                    self.players_connections[str(addr)] = conn
                    self.players_objects[str(addr)] = PlayerObject(100, 100)
                    self.players_data[str(addr)] = credentials
                    self.players_common_data[str(addr)] = {'player_color': credentials.get("player_color"),
                                                           NICKNAME: nickname
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

    def stop_server(self):
        try:
            self.socket.close()
            self.socket_opened = 0
            if self.game_thread_id:
                os.kill(self.game_thread_id, signal.SIGKILL)
        except Exception:
            pass

    def __del__(self):
        self.stop_server()

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
            self.disconnect_player(addr)


class ServerGame:
    TICK_RATE = 64

    def __init__(self, players_connections, server, cell_data, players_objects):
        self.server: Server = server
        self.players_connections: dict = players_connections

        self.players_data = {}  # data sent by players
        self.players_data_to_send = {}  # data which sends to players
        self.players_objects = players_objects

        self.clock = ROUND_CLOCK
        self.data_to_send = {}

        self.ARENA = ArenaCell(data=cell_data)

    def run(self):
        LOGGER.info('Sever Game loop started.')
        update_delay = 1 / self.TICK_RATE
        LOGGER.info(f'Tick rate {self.TICK_RATE}. Time per frame: {update_delay}')

        next_update = -1
        while True:
            t = time()
            if t > next_update:
                next_update = t + update_delay
                # logger.info(f'Game loop. Time: {self.clock.time}')
                self.clock.update(update_delay)
                self.UPDATE()
            elif next_update - t - 0.05 > 0.01:
                sleep(next_update - t - 0.05)

    def UPDATE(self):
        self.ARENA.update()
        self.data_to_send.clear()
        self.get_players_data()
        # if self.players_data:
        #     LOGGER.info(f"Info from players: {self.players_data}")

        self.data_to_send[PLAYERS_DATA] = self.players_data
        self.send_data_to_players()

    def game_finished(self):
        self.server.finish_game()

    def get_players_data(self):
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
                    player.angle = data.get('angle')
                    player_action = player.update(commands=data.get('keyboard'),
                                                  mouse_buttons=data.get('mouse_data')[0],
                                                  mouse_pos=data.get('mouse_data')[1])

                    self.players_data[str(addr)] = {
                        'position': player.position,
                        'angle': player.angle,
                        'player_action': player_action,
                    }

    def send_data_to_players(self):
        if self.server.server_actions:
            self.data_to_send[SERVER_ACTION] = self.server.server_actions.copy()

        self.data_to_send[SERVER_TIME] = self.clock()
        self.server.server_actions.clear()
        json_data = json.dumps(self.data_to_send).encode()

        for addr, sock in self.players_connections.copy().items():
            try:

                sock.send(json_data)
            except Exception as e:
                self.server.disconnect_player(addr)

        self.data_to_send.clear()

    def __del__(self):
        LOGGER.info(f'Game server was closed.')


if __name__ == '__main__':
    try:
        Server()
    except Exception as e:
        LOGGER.critical(e)
        print(e)
        raise Exception(e)
