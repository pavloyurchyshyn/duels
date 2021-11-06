from settings.global_parameters import GLOBAL_SETTINGS
from settings.window_settings import HALF_SCREEN_W, HALF_SCREEN_H, MAIN_SCREEN
from settings.UI_setings.button_settings import DEFAULT_BUTTON_X_SIZE
from settings.game_stages_constants import TEST_DRAW_CONST
from common_things.stages import Stages

PAUSE_MAIN_SCREEN_COPY = MAIN_SCREEN.copy()
PAUSE_SCREEN = MAIN_SCREEN.copy()


def test_draw():
    GLOBAL_SETTINGS[TEST_DRAW_CONST] = not GLOBAL_SETTINGS[TEST_DRAW_CONST]


ROUND_PAUSE_BUTTONS = {
    '_continue': {
        'args': (),
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2,
            'y': 300,
            'text': 'Continue',
            'on_click_action': Stages().set_round_stage,
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
            'active': 1,
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
            'active': 1,
            'visible': False,
            'non_visible_after_click': 1,
            'non_active_after_click': 1,

        }
    }
}
