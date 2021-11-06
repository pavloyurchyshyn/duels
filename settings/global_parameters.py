from time import time as current_time
from settings.game_stages_constants import *
GLOBAL_SETTINGS = {
    'current_stage': 'main_menu',
    'test_draw': 0,
    'next_pause': -1,
    'pause_delay': 0.5,
}


def pause_available() -> bool:
    return GLOBAL_SETTINGS['next_pause'] < current_time()


def pause_step():
    GLOBAL_SETTINGS['next_pause'] = GLOBAL_SETTINGS['pause_delay'] + current_time()

def change_test_draw_status():
    GLOBAL_SETTINGS[TEST_DRAW_CONST] = not GLOBAL_SETTINGS[TEST_DRAW_CONST]