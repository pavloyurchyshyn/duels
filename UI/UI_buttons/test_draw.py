from UI.UI_base.button_UI import Button
from settings.global_parameters import GLOBAL_SETTINGS
from settings.colors import WHITE, GREY_GREEN, GREY_RED
from settings.game_stages import TEST_DRAW_S, MULTIPLAYER_MENU_S, EXIT_S
from settings.window_settings import MAIN_SCREEN


def test_draw():
    GLOBAL_SETTINGS[TEST_DRAW_S] = not GLOBAL_SETTINGS[TEST_DRAW_S]


button = {
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
    'text_non_active_color': WHITE,
    'active_pic': not GLOBAL_SETTINGS[TEST_DRAW_S],
    'screen': MAIN_SCREEN,
}

TEST_DRAW_BUTTON = Button(**button)
