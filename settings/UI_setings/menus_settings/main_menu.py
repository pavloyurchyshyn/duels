from settings.global_parameters import GLOBAL_SETTINGS
from settings.colors import WHITE, GREY_GREEN, GREY_RED
from settings.window_settings import HALF_SCREEN_W
from settings.UI_setings.button_settings import DEFAULT_BUTTON_X_SIZE
from settings.game_stages import MAIN_MENU_SETTINGS, CURRENT_STAGE, START, TEST_DRAW

from common_things.close_game import close_game
from common_things.global_clock import ROUND_CLOCK


def start_game():
    GLOBAL_SETTINGS[CURRENT_STAGE] = START
    ROUND_CLOCK.reload()


def test_draw():
    GLOBAL_SETTINGS[TEST_DRAW] = not GLOBAL_SETTINGS[TEST_DRAW]


def settings():
    GLOBAL_SETTINGS[CURRENT_STAGE] = MAIN_MENU_SETTINGS


MAIN_MENU_BUTTONS = {
    # test draw button 
    '_test_draw': {
        'args': (),
        'kwargs': {
            'x': 50,
            'y': 50,
            'text': 'Turn On TEST_DRAW',
            'non_active_text': 'Turn Off TEST_DRAW',
            'on_click_action': test_draw,
            'non_active_after_click': 0,
            'change_after_click': 1,
            'text_size': 10,
            'border_color': GREY_GREEN,
            'border_non_active_color': GREY_RED,
            # 'text_color': WHITE,
            'text_non_active_color': WHITE,
            'active_pic': not GLOBAL_SETTINGS[TEST_DRAW]
        }
    },
    '_exit': {
        'args': (),
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2,
            'y': 700,
            'text': 'EXIT',
            'on_click_action': close_game,
        }
    },

    'start': {
        'args': (HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2, 500),
        'kwargs': {
            'active': 0,
            'text': 'START',
            'on_click_action': start_game,
        },
    },

    '_settings': {
        'args': (),
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2,
            'y': 600,
            'text': 'Settings',
            'on_click_action': settings,
        }
    },
}
