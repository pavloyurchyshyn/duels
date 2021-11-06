from common_things.stages import Stages

from settings.screen_size import HALF_SCREEN_W, HALF_SCREEN_H, SCREEN_H, SCREEN_W  # , X_SCALE, Y_SCALE

from settings.UI_setings.button_settings import DEFAULT_BUTTON_X_SIZE

from common_things.global_clock import ROUND_CLOCK
from UI.UI_controller import UI_TREE

STAGES = Stages()


def start_game():
    STAGES.set_start_round_stage()
    ROUND_CLOCK.reload()


MAIN_MENU_BUTTONS = {
    'start': {
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2,
            'p_y_pos': 0.455,
            'active': 1,
            'text': 'START',
            'on_click_action': start_game,
            'id': 'menu_start',
        },
    },

    'multiplayer': {
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2,
            'p_y_pos': 0.555,
            'text': 'Multiplayer',
            # 'active': False,
            'on_click_action': STAGES.set_multiplayer_menu_stage,
            'id': 'menu_multiplayer',

        }
    },

    '_settings': {
        'args': (),
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2,
            'p_y_pos': 0.648,
            'text': 'Settings',
            'on_click_action': STAGES.set_main_menu_settings_stage,
            'id': 'menu_settings',

        }
    },
    '_exit': {
        'args': (),
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2,
            'p_y_pos': 0.74,
            'text': 'EXIT',
            'id': 'menu_exit',
            'on_click_action': UI_TREE.drop_focused

        }
    },
    '_exit_yes': {
        'args': (),
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE,
            'p_y_pos': 0.5,
            'text': 'YES',
            'active': 0,
            'visible': False,
            'on_click_action': STAGES.set_exit_stage,
            'non_visible_after_click': 1,
            'non_active_after_click': 1,
            'id': 'menu_exit_yes',
            'border_non_active_color': (255, 255, 255),
            'text_non_active_color': (255, 255, 255)
        }
    },

    '_exit_no': {
        'args': (),
        'kwargs': {
            'x': HALF_SCREEN_W + DEFAULT_BUTTON_X_SIZE // 2,
            'p_y_pos': 0.5,
            'text': 'NO',
            'active': 0,
            'visible': False,
            'non_visible_after_click': 1,
            'non_active_after_click': 1,
            'id': 'menu_exit_no',
            'border_non_active_color': (255, 255, 255),
            'text_non_active_color': (255, 255, 255)
        }
    }

}
