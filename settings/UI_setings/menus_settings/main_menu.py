from common_things.stages import Stages

from settings.screen_size import HALF_SCREEN_W
from settings.colors import BLACK
from settings.UI_setings.button_settings import DEFAULT_BUTTON_X_SIZE

from common_things.global_clock import ROUND_CLOCK
from UI.UI_controller import UI_TREE
from common_things.sprites_functions import get_surface
from settings.window_settings import SCREEN_W, SCREEN_H, MAIN_SCREEN
from settings.game_stages_constants import MAIN_MENU_STAGE

# SURFACE = get_surface(SCREEN_W, SCREEN_H)
STAGES = Stages()
EXIT_WARNING = {'ex_warn': 0}


def exit_warning():
    return EXIT_WARNING['ex_warn']


def change_exit_warn(val):
    EXIT_WARNING['ex_warn'] = val


def start_game():
    STAGES.set_start_round_stage()
    ROUND_CLOCK.reload()


MENU_EXIT_YES_ID = 'menu_exit_yes'
MENU_EXIT_NO_ID = 'menu_exit_no'
MENU_START_ID = 'menu_start'
MENU_MULTIPLAYER_ID = 'menu_multiplayer'
MENU_SETTINGS_ID = 'menu_settings'
MENU_EXIT_ID = 'menu_exit'


def activate_exit_warning_message():
    change_exit_warn(1)

    exit_yes = UI_TREE.get_element(MAIN_MENU_STAGE, MENU_EXIT_YES_ID)
    exit_yes.make_active()
    exit_yes.make_visible()

    exit_no = UI_TREE.get_element(MAIN_MENU_STAGE, MENU_EXIT_NO_ID)
    exit_no.make_active()
    exit_no.make_visible()

    UI_TREE.get_element(MAIN_MENU_STAGE, MENU_START_ID).make_inactive()
    UI_TREE.get_element(MAIN_MENU_STAGE, MENU_MULTIPLAYER_ID).make_inactive()
    UI_TREE.get_element(MAIN_MENU_STAGE, MENU_SETTINGS_ID).make_inactive()
    UI_TREE.get_element(MAIN_MENU_STAGE, MENU_EXIT_ID).make_inactive()
    UI_TREE.drop_focused()


def deactivate_exit_warning_message():
    change_exit_warn(0)

    # SURFACE.fill(BLACK)
    exit_yes = UI_TREE.get_element(MAIN_MENU_STAGE, MENU_EXIT_YES_ID)
    exit_yes.make_inactive()
    exit_yes.make_invisible()

    exit_no = UI_TREE.get_element(MAIN_MENU_STAGE, MENU_EXIT_NO_ID)
    exit_no.make_inactive()
    exit_no.make_invisible()

    UI_TREE.get_element(MAIN_MENU_STAGE, MENU_START_ID).make_active()
    UI_TREE.get_element(MAIN_MENU_STAGE, MENU_MULTIPLAYER_ID).make_active()
    UI_TREE.get_element(MAIN_MENU_STAGE, MENU_SETTINGS_ID).make_active()
    UI_TREE.get_element(MAIN_MENU_STAGE, MENU_EXIT_ID).make_active()
    UI_TREE.drop_focused()


MAIN_MENU_BUTTONS = {
    'start': {
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2,
            'p_y_pos': 0.455,
            'active': 1,
            'text': 'START',
            'on_click_action': start_game,
            'id': MENU_START_ID,
        },
    },

    'multiplayer': {
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2,
            'p_y_pos': 0.555,
            'text': 'Multiplayer',
            # 'active': False,
            'on_click_action': STAGES.set_multiplayer_menu_stage,
            'id': MENU_MULTIPLAYER_ID,

        }
    },

    '_settings': {
        'args': (),
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2,
            'p_y_pos': 0.648,
            'text': 'Settings',
            'on_click_action': STAGES.set_main_menu_settings_stage,
            'id': MENU_SETTINGS_ID,

        }
    },
    '_exit': {
        'args': (),
        'kwargs': {
            'x': HALF_SCREEN_W - DEFAULT_BUTTON_X_SIZE // 2,
            'p_y_pos': 0.74,
            'text': 'EXIT',
            'id': MENU_EXIT_ID,
            'on_click_action': activate_exit_warning_message,
            'border_non_active_color': (255, 255, 255),
            'text_non_active_color': (255, 255, 255)

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
            'id': MENU_EXIT_YES_ID,
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
            'id': MENU_EXIT_NO_ID,
            'border_non_active_color': (255, 255, 255),
            'text_non_active_color': (255, 255, 255),
            'on_click_action': deactivate_exit_warning_message
        }
    }

}
