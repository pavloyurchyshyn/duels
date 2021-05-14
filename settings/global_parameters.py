from time import time as cur_time

GLOBAL_SETTINGS = {
    'current_stage': 'main_menu',
    'current_cell': None,
    'test_draw': 0,
    'PAUSE': False,
    'next_pause': cur_time(),
    'pause_delay': 0.5,
}
