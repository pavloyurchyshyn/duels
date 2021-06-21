from pygame import font
import os
VERSION = '0.0.1'

FPS = 64


def custom_font_size(size: int):
    return font.SysFont('Arial', size)


DEFAULT_FONT_SIZE = 25
DEFAULT_FONT = font.SysFont('Arial', DEFAULT_FONT_SIZE)

ROOT_OF_GAME = os.path.abspath(os.getcwd())
SETTINGS_PATH = os.path.join(ROOT_OF_GAME, 'settings')
SOUNDS_FOLDER = os.path.join(ROOT_OF_GAME, 'sounds')
SERVER_FOLDER = os.path.join(ROOT_OF_GAME, 'network')

COMMON_GAME_SETTINGS_JSON_PATH = os.path.join(SETTINGS_PATH, 'common_game_settings.json')

PLAYER_NICKNAME_KEY = 'player_nickname'