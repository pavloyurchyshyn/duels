from time import time as current_time
from settings.game_stages_constants import *

GLOBAL_SETTINGS = {
    'current_stage': 'main_menu',
    'test_draw': 0,
    'next_pause': -1,
    'pause_delay': 0.5,
}


def get_current_stage():
    return GLOBAL_SETTINGS[CURRENT_STAGE]


def change_test_draw_status():
    GLOBAL_SETTINGS[TEST_DRAW_CONST] = not GLOBAL_SETTINGS[TEST_DRAW_CONST]


def pause_available() -> bool:
    return GLOBAL_SETTINGS['next_pause'] < current_time()


def pause_step():
    GLOBAL_SETTINGS['next_pause'] = GLOBAL_SETTINGS['pause_delay'] + current_time()


def change_current_stage(stage):
    GLOBAL_SETTINGS[CURRENT_STAGE] = stage


def set_start_round_stage() -> None:
    change_current_stage(START_ROUND_STAGE)


def set_round_stage() -> None:
    change_current_stage(ROUND_STAGE)


def set_round_pause_stage() -> None:
    change_current_stage(ROUND_PAUSE_STAGE)


def set_main_menu_stage() -> None:
    change_current_stage(MAIN_MENU_STAGE)


def set_loading_stage() -> None:
    change_current_stage(LOADING_STAGE)


def set_main_menu_settings_stage() -> None:
    change_current_stage(MAIN_MENU_SETTINGS_STAGE)


def set_multiplayer_menu_stage() -> None:
    change_current_stage(MULTIPLAYER_MENU_STAGE)


def set_multiplayers_round_stage() -> None:
    change_current_stage(MULTIPLAYER_CLIENT_ROUND_STAGE)


def set_multiplayers_round_pause_stage() -> None:
    change_current_stage(MULTIPLAYER_CLIENT_ROUND_PAUSE_STAGE)


def set_multiplayers_disconnect_stage() -> None:
    change_current_stage(MULTIPLAYER_CLIENT_DISCONNECT_STAGE)


def set_exit_stage() -> None:
    change_current_stage(EXIT_STAGE)
