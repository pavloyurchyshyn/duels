from settings.global_parameters import GLOBAL_SETTINGS
from settings.colors import WHITE, GREY_GREEN, GREY_RED
from settings.window_settings import SCREEN_W
from settings.UI_setings.button_settings import DEFAULT_BUTTON_X_SIZE
from settings.game_stages import MAIN_MENU_SETTINGS_S, CURRENT_STAGE, START_ROUND_S, TEST_DRAW_S, MAIN_MENU_S
from common_things.close_game import close_game


def back_to_menu():
    GLOBAL_SETTINGS[CURRENT_STAGE] = MAIN_MENU_S


MAIN_MENU_SETTINGS_BUTTONS = {
    '_exit': {
        'args': (),
        'kwargs': {
            'size_x': 40,
            'size_y': 40,
            'x': SCREEN_W - 55,
            'y': 10,
            'text': 'X',
            'on_click_action': back_to_menu,
        }
    },

}
