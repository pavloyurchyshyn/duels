from UI.UI_base.button_UI import Button
from settings.global_parameters import GLOBAL_SETTINGS
from settings.game_stages import TEST_DRAW_S, MULTIPLAYER_MENU_S, EXIT_S, CURRENT_STAGE, ROUND_PAUSE_S
from settings.window_settings import MAIN_SCREEN, SCREEN_W
from settings.UI_setings.menus_settings.round_pause import PAUSE_MAIN_SCREEN_COPY
from UI.UI_menus.round_pause import ROUND_PAUSE_UI


def round_pause():
    GLOBAL_SETTINGS[CURRENT_STAGE] = ROUND_PAUSE_S
    PAUSE_MAIN_SCREEN_COPY.blit(MAIN_SCREEN, (0, 0))
    ROUND_PAUSE_UI.draw_round()


button = {
    'screen': MAIN_SCREEN,
    'x': SCREEN_W - 55,
    'y': 10,
    'size_x': 40,
    'size_y': 40,
    'text': 'X',
    'on_click_action': round_pause,
}

ROUND_PAUSE_BUTTON = Button(**button)
