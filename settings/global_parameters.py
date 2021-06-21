from time import time as cur_time
import os

GLOBAL_SETTINGS = {
    'current_stage': 'main_menu',
    'current_cell': None,
    'test_draw': 0,
    'next_pause': -1,
    'pause_delay': 0.5,
}


def pause_available() -> bool:
    return GLOBAL_SETTINGS['next_pause'] < cur_time()


def pause_step():
    GLOBAL_SETTINGS['next_pause'] = GLOBAL_SETTINGS['pause_delay'] + cur_time()
