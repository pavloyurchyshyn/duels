from UI.UI_base.button_UI import Button
# from settings.global_parameters import change_test_draw_status
from settings.colors import WHITE, GREY_GREEN, GREY_RED
from settings.global_parameters import set_slow_motion
from settings.window_settings import MAIN_SCREEN


button = {
    'p_x_pos': 0.93,
    'p_y_pos': 0.95,
    'text': 'Slow',
    # 'non_active_text': 'X',
    'on_click_action': set_slow_motion,
    'non_active_after_click': 0,
    'change_after_click': 0,
    'text_size': 10,
    'border_color': GREY_GREEN,
    'border_non_active_color': GREY_RED,
    'text_non_active_color': WHITE,
    'screen': MAIN_SCREEN,
    'size_x': 50, 'size_y': 50,

}

SLOW_MOTION_BUTTON = Button(**button)
