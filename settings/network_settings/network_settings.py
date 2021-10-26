from settings.common_settings import COMMON_GAME_SETTINGS_JSON_PATH
from settings.network_settings.network_constants import *
from common_things.save_and_load_json_config import get_parameter_from_json_config
from settings.players_settings.player_settings import PLAYER_SIZE
import socket

DEFAULT_PORT = 8002

GAME_TICK_RATE = 64

DEFAULT_TIME_PER_ROUND = 60
END_ROUND_TIME = -5  # seconds
TIME_TO_START_ROUND = -10
WAIT_FOR_PLAYERS_TIME = -60

CONNECTION_TIMEOUT = 15

SERVER_FILE_NAME = 'server.py'

NETWORK_DATA = {
    IP: socket.gethostbyname(socket.gethostname()),
    PORT: DEFAULT_PORT,
    NICKNAME: get_parameter_from_json_config("player_nickname", COMMON_GAME_SETTINGS_JSON_PATH, ''),
    PASSWORD: '.',
    PLAYERS_NUMBER: 2,
}


def update_host_address(text):
    text = text.split(':')
    NETWORK_DATA['ip'] = text[0]
    NETWORK_DATA['port'] = text[1]


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


SERVER_ARGUMENTS = {
    f'--{PORT}': [DEFAULT_PORT, 'Server Port'],
    f'--{PLAYERS_NUMBER}': [2, 'Number of players'],
    f'--{PASSWORD}': ['.', 'Lobby password'],
    f'--{ROUNDS}': [2, 'Needed round to win'],
    f'--{TIME_PER_ROUND}': [DEFAULT_TIME_PER_ROUND, 'Time for round in minutes'],
    f'--{GAME_MODE}': [CLASSIC_GAME_MODE, 'Mode of game.'],
    f'--{PLAYER_SIZE_ARG}': [PLAYER_SIZE, 'Player_size'],
    f'--{TEAM_NAMES}': ['red,blue', 'Coma separated teams names'],
    f'--{ADMIN_AK}': ['None', 'Admin access key'],
}
