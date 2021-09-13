from settings.global_parameters import set_start_round_stage, set_main_menu_settings_stage, set_exit_stage, set_multiplayer_menu_stage

from settings.screen_size import HALF_SCREEN_W, HALF_SCREEN_H, SCREEN_H, SCREEN_W, X_SCALE, Y_SCALE
from settings.UI_setings.button_settings import DEFAULT_BUTTON_X_SIZE

from common_things.global_clock import ROUND_CLOCK


def start_game():
    set_start_round_stage()
    ROUND_CLOCK.reload()


MAIN_MENU_BUTTONS = {
    'start': {
        'args': (HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2, 500 * Y_SCALE),
        'kwargs': {
            'active': 1,
            'text': 'START',
            'on_click_action': start_game,
        },
    },

    'multiplayer': {
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2,
            'y': int(SCREEN_H * 0.555),
            'text': 'Multiplayer',
            # 'active': False,
            'on_click_action': set_multiplayer_menu_stage,

        }
    },

    '_settings': {
        'args': (),
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2,
            'y': int(SCREEN_H * 0.648),
            'text': 'Settings',
            'on_click_action': set_main_menu_settings_stage,
        }
    },
    '_exit': {
        'args': (),
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2,
            'y': int(SCREEN_H * 0.74),
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
            'on_click_action': set_exit_stage,
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
