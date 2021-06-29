import socket

from _thread import *
import sys
import os
import signal
import logging
import datetime
import json
from time import time, sleep
from argparse import ArgumentParser


# from settings.network_settings import DEFAULT_PORT, anon_host
# from common_things.global_clock import Clock
class Clock:
    def __init__(self, time=0, d_time=0):
        self._time = time
        self._d_time = d_time

    @property
    def time(self):
        return self._time

    @property
    def d_time(self):
        return self._d_time

    def update(self, d_time):
        """
        d_time in milliseconds
        """
        self._d_time = d_time
        self._time += d_time

    def __call__(self, *args, **kwargs):
        return self._time, self._d_time

    def reload(self):
        self._d_time = self._time = 0

    def set_time(self, time, d_time):
        self._time, self._d_time = time, d_time


def anon_host(host):
    if type(host) is tuple:
        host = f"{host[0]}:{host[1]}"
    host = host.strip()
    host = host.split(':')[0]
    pre, post = host[:2], host[-2:]
    host = host[2:-2]

    for i in range(0, 10):
        host = host.replace(str(i), '*')

    host = f'{pre}{host}{post}'
    return f'{host}'


DEFAULT_PORT = 8000

PORT = 'port'
NICKNAME = 'nickname'
PASSWORD = 'password'

ROOT_OF_GAME = os.path.abspath(os.getcwd())
LOGS_FOLDER = os.path.join(ROOT_OF_GAME, 'logs')
START = datetime.datetime.today().strftime("%Y-%m-%d-%H.%M.%S")

DISCONNECT_TIMEOUT = 60


class Server:
    ARGUMENTS = {
        '--port': ['DEFAULT_PORT', 'Server Port'],
        '--pnum': ['2', 'Number of players'],
        '--password': ['', 'Lobby password'],
    }

    def __init__(self):
        self.address = socket.gethostbyname(socket.gethostname())
        self.port = DEFAULT_PORT

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.players_number = 2
        self.players_connected = 0

        self.password = ''

        self.parse_args()

        self.socket.bind((self.address, self.port))
        self.socket.listen()
        self.socket_opened = 1

        self.players = {}
        self.players_name = {}

        self.SERVER_GAME = ServerGame(self.players, self)

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

    def run(self):
        logger.info(f'Server started {START} {self.address}:{self.port}')

        while self.socket_opened:
            conn, addr = self.socket.accept()
            logger.info(f'Accepted: {conn, anon_host(addr)}')

            if self.players_connected >= self.players_number:
                conn.send('Connection limit. Disconnect.'.encode())
                conn.close()
                logger.info(f'Connection limit {self.players_connected}/{self.players_number}. Disconnected {anon_host(addr)}')

            else:
                recv = conn.recv(2048).decode()
                credentials = json.loads(recv)
                logger.info(f'Credentials: {credentials}')

                if credentials[PASSWORD] == self.password:
                    logger.info(f'Password is good! {credentials[PASSWORD]} == {self.password}')
                    self.players_connected += 1
                    nickname = credentials[NICKNAME]

                    same_nick_count = sum([1 for nick in self.players_name if nick == nickname or nick.startswith(f'{nickname}(')])
                    if nickname in self.players_name:
                        nickname = f'{nickname}({same_nick_count})'

                    self.players_name[nickname] = addr
                    conn.send(f'Connected to {anon_host(self.address)}'.encode())
                    logger.info(
                        f'Connected. {anon_host(addr)}. Player #{self.players_connected}. Nickname {nickname}')
                    self.players[addr] = conn
                else:
                    logger.info(f'Failed to connect. {anon_host(addr)}. Nickname {credentials[NICKNAME]}')
                    logger.info(f'Bad password! {credentials[PASSWORD]} != {self.password}')

    def disconnect_player(self, addr, del_player=False):
        try:
            self.players[addr].close()
        except Exception as e:
            logger.error(f"Failed to disconnect {addr}: \n\t{e}")
        else:
            logger.info(f'Player {addr} disconnected successfully.')

        if del_player:
            self.players.pop(addr)

        self.players_number -= 1
        logger.info(f'Players number: {self.players_number}')

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

        # player_soc.send(str.encode(make_pos(pos[player])))
        # reply = ""
        # while True:
        #     # try:
        #     data = read_pos(conn.recv(2048).decode())
        #     pos[player] = data
        #     # print(f'Player {player}, data {data}')
        #     if not data:
        #         print("Disconnected")
        #         break
        #     else:
        #         if player == 1:
        #             reply = pos[0]
        #         else:
        #             reply = pos[1]
        #
        #         # print("Received: ", data)
        #         # print("Sending : ", reply)
        #
        #     conn.sendall(str.encode(make_pos(reply)))
        #     # except Exception as e:
        #     #     print(e)
        #     #     break
        #
        # print("Lost connection")
        # server_con.disconnect_player(player_addr)


class ServerGame:
    TICK_RATE = 64

    def __init__(self, players, server):
        self.server = server
        self.players: dict = players
        self.players_data = {}  # data sent by players
        self.players_data_to_send = {}  # data which sends to players
        self.clock = Clock()
        self.data_to_send = {}

    def run(self):
        logger.info('Sever Game loop started.')
        update_delay = 1 / self.TICK_RATE
        logger.info(f'Tick rate {self.TICK_RATE}. Time per frame: {update_delay}')

        next_update = -1
        while True:
            t = time()
            if t > next_update:
                next_update = t + update_delay
                # logger.info(f'Game loop. Time: {self.clock.time}')
                self.clock.update(update_delay)

                self.get_players_data()
                self.send_data_to_players()
            elif next_update - t - 0.05 > 0.01:
                sleep(next_update - t - 0.05)

    def game_finished(self):
        self.server.finish_game()

    def get_players_data(self):
        self.players_data.clear()
        for addr, conn in self.players.items():
            self.players_data[addr] = conn.recv(2048)

    def send_data_to_players(self):
        json_data = self.data_to_send
        for addr, sock in self.players.items():
            sock.send(json_data)

        self.data_to_send.clear()

    def __del__(self):
        logger.info(f'Game server was closed.')


if __name__ == '__main__':
    logging.basicConfig(filename=os.path.join(LOGS_FOLDER, "{}_server_logs.txt".format(START)), level=0)
    logger = logging.getLogger(__name__)
    Server()
# server = "192.168.0.105"
# port = 5555
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# try:
#     s.bind((server, port))
# except socket.error as e:
#     str(e)
#
# s.listen(2)
# print("Waiting for a connection, Server Started")
#
#
# def read_pos(string):
#     string = string.split(",")
#     # print(string)
#     return int(round(float(string[0]), 1)), int(round(float(string[1]), 1)), float(string[2])  # , float(string[3])
#
#
# def make_pos(tup):
#     return str(tup[0]) + "," + str(tup[1]) + ',' + str(tup[2]) + ','  # + str(tup[3])
#
#
# pos = [(100, 100, 0, 0), (100, 100, 0, 0)]
#
#
# def threaded_client(conn, player, addr):
#     conn.send(str.encode(make_pos(pos[player])))
#     reply = ""
#     while True:
#         # try:
#         data = read_pos(conn.recv(2048).decode())
#         pos[player] = data
#         # print(f'Player {player}, data {data}')
#         if not data:
#             print("Disconnected")
#             break
#         else:
#             if player == 1:
#                 reply = pos[0]
#             else:
#                 reply = pos[1]
#
#             # print("Received: ", data)
#             # print("Sending : ", reply)
#
#         conn.sendall(str.encode(make_pos(reply)))
#         # except Exception as e:
#         #     print(e)
#         #     break
#
#     print("Lost connection")
#     conn.close()
#
#
# print(socket.gethostbyname(socket.gethostname()))
#
# currentPlayer = 0
# threads = {}
# Server()
# while True:
#     conn, addr = s.accept()
#     conn.send(f'Connected to {anon_host(server)}'.encode())
#     print("Connected to:", addr)
#     conn.close()
#
#     idx = start_new_thread(threaded_client, (conn, currentPlayer, addr))
#     threads[currentPlayer] = idx
#     currentPlayer += 1
