from time import time as current_time

GLOBAL_SETTINGS = {
    'test_draw': 0,
    'next_pause': -1,
    'pause_delay': 0.25,
    'client_instance': 0,
}


def SET_CLIENT_INSTANCE(v=1):
    GLOBAL_SETTINGS['client_instance'] = v


def its_client_instance():
    return GLOBAL_SETTINGS['client_instance']


def pause_available() -> bool:
    return GLOBAL_SETTINGS['next_pause'] < current_time()


def pause_step():
    GLOBAL_SETTINGS['next_pause'] = GLOBAL_SETTINGS['pause_delay'] + current_time()


def change_test_draw_status():
    GLOBAL_SETTINGS['test_draw'] = not GLOBAL_SETTINGS['test_draw']


def test_draw_status_is_on():
    return GLOBAL_SETTINGS['test_draw']
