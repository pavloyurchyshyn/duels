from settings.global_parameters import GLOBAL_SETTINGS
from settings.window_settings import SCREEN_W
from settings.game_stages import CURRENT_STAGE, MAIN_MENU_S
from settings.window_settings import MAIN_SCREEN
from settings.colors import WHITE, GREY_DARK_2

from UI.UI_base.progress_bar_UI import Progress_Bar
from UI.UI_base.button_UI import Button

from common_things.sound_loader import GLOBAL_MUSIC_PLAYER


def back_to_menu():
    GLOBAL_SETTINGS[CURRENT_STAGE] = MAIN_MENU_S


def minus_music_volume():
    GLOBAL_MUSIC_PLAYER.minus_volume()
    VOLUME_PROGRESS_BAR.update(current_stage=GLOBAL_MUSIC_PLAYER.volume_stage,
                               bar_color=WHITE if not GLOBAL_MUSIC_PLAYER.muted else GREY_DARK_2)


def add_music_volume():
    GLOBAL_MUSIC_PLAYER.add_volume()
    VOLUME_PROGRESS_BAR.update(current_stage=GLOBAL_MUSIC_PLAYER.volume_stage,
                               bar_color=WHITE)
    MUTE_MUSIC.change_picture(active=1)


def mute_music_click():
    if GLOBAL_MUSIC_PLAYER.muted:
        GLOBAL_MUSIC_PLAYER.unmute()
        VOLUME_PROGRESS_BAR.update(current_stage=GLOBAL_MUSIC_PLAYER.volume_stage,
                                   bar_color=WHITE)
    else:
        GLOBAL_MUSIC_PLAYER.mute()
        VOLUME_PROGRESS_BAR.update(current_stage=GLOBAL_MUSIC_PLAYER.volume_stage,
                                   bar_color=GREY_DARK_2)


MUSIC_VOLUME_VALUE = Button(x=50, y=100,
                            text=f'Music Volume:',
                            screen=MAIN_SCREEN,
                            border_width=0,
                            transparent=1)

VOLUME_PROGRESS_BAR = Progress_Bar(screen=MAIN_SCREEN,
                                   stage=GLOBAL_MUSIC_PLAYER.volume_stage,
                                   stages_num=GLOBAL_MUSIC_PLAYER.volume_stages,
                                   bar_pos=(300, 125),
                                   bar_inner_color=GREY_DARK_2 if GLOBAL_MUSIC_PLAYER.muted else WHITE,
                                   bar_x_size=200)

MUTE_MUSIC = Button(**{
    'x': 600,
    'y': 100,
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
    'screen': MAIN_SCREEN
})

MAIN_MENU_SETTINGS_BUTTONS = {
    '_sound_minus': {
        'kwargs': {
            'size_x': 40,
            'size_y': 40,
            'x': 250,
            'y': 100,
            'text': '-',
            'on_click_action': minus_music_volume,
        }
    },

    '_sound_add': {
        'kwargs': {
            'size_x': 40,
            'size_y': 40,
            'x': 550,
            'y': 100,
            'text': '+',
            'on_click_action': add_music_volume,
        }
    },

    '_exit': {
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
