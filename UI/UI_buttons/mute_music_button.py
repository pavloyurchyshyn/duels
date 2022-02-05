# from settings.screen_size import X_SCALE, Y_SCALE
X_SCALE, Y_SCALE = 1, 1

from UI.UI_base.button_UI import Button
from common_things.sound_loader import GLOBAL_MUSIC_PLAYER
from settings.colors import WHITE, GREY_DARK_2
from settings.window_settings import MAIN_SCREEN
from UI.UI_buttons.music_volume_progress_bar import VOLUME_PROGRESS_BAR

MUTE_MUSIC_ID = 'music_mute'


def mute_music_click():
    if GLOBAL_MUSIC_PLAYER.muted:
        GLOBAL_MUSIC_PLAYER.unmute()
        VOLUME_PROGRESS_BAR.update(current_stage=GLOBAL_MUSIC_PLAYER.volume_stage,
                                   bar_color=WHITE)
    else:
        GLOBAL_MUSIC_PLAYER.mute()
        VOLUME_PROGRESS_BAR.update(current_stage=GLOBAL_MUSIC_PLAYER.volume_stage,
                                   bar_color=GREY_DARK_2)


MUTE_MUSIC_BUTTON = Button(**{
    'x': 600 * X_SCALE,
    'y': 100 * Y_SCALE,
    'size_x': 40,
    'size_y': 40,
    'text': ' ',
    'non_active_text': 'X',
    'on_click_action': mute_music_click,
    'non_active_after_click': 0,
    'change_after_click': 1,
    'border_color': WHITE,
    'border_non_active_color': WHITE,
    'text_non_active_color': WHITE,
    'active_pic': not GLOBAL_MUSIC_PLAYER.muted,
    'screen': MAIN_SCREEN,
    'id': MUTE_MUSIC_ID,
    'border_width': 1,
})
