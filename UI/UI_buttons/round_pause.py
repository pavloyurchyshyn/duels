from UI.UI_base.button_UI import Button
from settings.window_settings import MAIN_SCREEN, SCREEN_W
from settings.UI_setings.menus_settings.round_pause import PAUSE_MAIN_SCREEN_COPY
from UI.UI_menus.round_pause import ROUND_PAUSE_UI
from common_things.stages import Stages


def round_pause():
    Stages().set_round_pause_stage()
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
