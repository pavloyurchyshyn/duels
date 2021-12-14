from UI.UI_base.button_UI import Button
from settings.global_parameters import change_test_draw_status
from settings.colors import WHITE, GREY_GREEN, GREY_RED
from settings.global_parameters import test_draw_status_is_on
from settings.window_settings import MAIN_SCREEN


button = {
    'p_x_pos': 0.01,
    'p_y_pos': 0.01,
    'text': 'Turn On TEST_DRAW',
    'non_active_text': 'Turn Off TEST_DRAW',
    'on_click_action': change_test_draw_status,
    'non_active_after_click': 0,
    'change_after_click': 1,
    'text_size': 10,
    'border_color': GREY_GREEN,
    'border_non_active_color': GREY_RED,
    'text_non_active_color': WHITE,
    'active_pic': test_draw_status_is_on,
    'screen': MAIN_SCREEN,
}

TEST_DRAW_BUTTON = Button(**button)
