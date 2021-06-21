from settings.global_parameters import GLOBAL_SETTINGS
from settings.colors import WHITE, GREY_GREEN, GREY_RED
from settings.window_settings import HALF_SCREEN_W, HALF_SCREEN_H, MAIN_SCREEN
from settings.UI_setings.button_settings import DEFAULT_BUTTON_X_SIZE
from settings.game_stages import MAIN_MENU_SETTINGS_S, CURRENT_STAGE, START_ROUND_S, TEST_DRAW_S, MULTIPLAYER_MENU_S, EXIT_S

from common_things.global_clock import ROUND_CLOCK


def start_game():
    GLOBAL_SETTINGS[CURRENT_STAGE] = START_ROUND_S
    ROUND_CLOCK.reload()


def test_draw():
    GLOBAL_SETTINGS[TEST_DRAW_S] = not GLOBAL_SETTINGS[TEST_DRAW_S]


def settings():
    GLOBAL_SETTINGS[CURRENT_STAGE] = MAIN_MENU_SETTINGS_S


def multiplayer():
    GLOBAL_SETTINGS[CURRENT_STAGE] = MULTIPLAYER_MENU_S


def close_game():
    GLOBAL_SETTINGS[CURRENT_STAGE] = EXIT_S


MAIN_MENU_BUTTONS = {
    'start': {
        'args': (HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2, 500),
        'kwargs': {
            'active': 1,
            'text': 'START',
            'on_click_action': start_game,
        },
    },

    'multiplayer': {
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2,
            'y': 600,
            'text': 'Multiplayer',
            # 'active': False,
            'on_click_action': multiplayer,

        }
    },

    '_settings': {
        'args': (),
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2,
            'y': 700,
            'text': 'Settings',
            'on_click_action': settings,
        }
    },
    '_exit': {
        'args': (),
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2,
            'y': 800,
            'text': 'EXIT',
        }
    },
    '_exit_yes': {
        'args': (),
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE,
            'y': HALF_SCREEN_H,
            'text': 'YES',
            'active': False,
            'visible': False,
            'on_click_action': close_game,
            'non_visible_after_click': 1,
            'non_active_after_click': 1,

        }
    },

    '_exit_no': {
        'args': (),
        'kwargs': {
            'x': HALF_SCREEN_W + DEFAULT_BUTTON_X_SIZE // 2,
            'y': HALF_SCREEN_H,
            'text': 'NO',
            'active': False,
            'visible': False,
            'non_visible_after_click': 1,
            'non_active_after_click': 1,

        }
    }

}
