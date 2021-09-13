from settings.global_parameters import GLOBAL_SETTINGS
from settings.window_settings import HALF_SCREEN_W, HALF_SCREEN_H, MAIN_SCREEN
from settings.UI_setings.button_settings import DEFAULT_BUTTON_X_SIZE
from settings.game_stages_constants import MAIN_MENU_SETTINGS_STAGE, CURRENT_STAGE, START_ROUND_STAGE, TEST_DRAW_CONST, ROUND_STAGE, MAIN_MENU_STAGE

PAUSE_MAIN_SCREEN_COPY = MAIN_SCREEN.copy()
PAUSE_SCREEN = MAIN_SCREEN.copy()


def test_draw():
    GLOBAL_SETTINGS[TEST_DRAW_CONST] = not GLOBAL_SETTINGS[TEST_DRAW_CONST]


def continue_round():
    GLOBAL_SETTINGS[CURRENT_STAGE] = ROUND_STAGE


ROUND_PAUSE_BUTTONS = {

    '_continue': {
        'args': (),
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2,
            'y': 300,
            'text': 'Continue',
            'on_click_action': continue_round,
        }
    },

    '_exit': {
        'args': (),
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2,
            'y': 700,
            'text': 'To Menu',
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
