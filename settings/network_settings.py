from settings.common_settings import COMMON_GAME_SETTINGS_JSON_PATH
from common_things.save_and_load_json_config import get_parameter_from_json_config
import socket

DEFAULT_PORT = 8002

CONNECTED_MESSAGE = 'Connected {}'
BAD_PASSWORD = 'Bad password {}'

# CONSTANTS
IP = 'ip'
PORT = 'port'
NICKNAME = 'nickname'
PASSWORD = 'password'
PLAYERS_NUMBER = 'players_number'

DELETE_PLAYERS = 'dlt_players'
DELETE_PLAYER = 'dlt_player'
SERVER_ACTION = 'server_actions'
PLAYERS_DATA = 'players_data'
SERVER_TIME = 'server_time'

PREPARING = 'preparing_to_round'
PLAYER_LOADED = 'loaded'

TEAM_SCORES = 'teams_scores'
CURRENT_ROUND = 'current_round'
ROUND_FINISHED = 'round_finished'
ROUND_WINNER = 'round_winner'
TEAM_GAME_WON = 'game_finished'
GAME_WINNER = 'game_winner'

# PLAYERS ACTIONS
DAMAGED = 'damaged'
DEAD = 'dead'

DEFAULT_TIME_PER_ROUND = 3

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
