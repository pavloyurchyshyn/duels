from settings.global_parameters import GLOBAL_SETTINGS
from settings.window_settings import SCREEN_W
from settings.game_stages import CURRENT_STAGE, MAIN_MENU_S
from settings.window_settings import MAIN_SCREEN
from settings.colors import WHITE, GREY_DARK_2, GREY_BLUE, GREY_RED, GREY_GREEN, PLAYERS_COLORS
from settings.players_settings.player_settings import PLAYER_SIZE
from settings.common_settings import COMMON_GAME_SETTINGS_JSON_PATH as CGSJP

from UI.UI_base.progress_bar_UI import Progress_Bar
from UI.UI_base.button_UI import Button
from UI.UI_base.input_element_UI import InputElement

from common_things.sound_loader import GLOBAL_MUSIC_PLAYER
from common_things.save_and_load_json_config import get_parameter_from_json_config, change_parameter_in_json_config
from common_things.img_loader import normalize_color
from player_and_spells.player.simple_player import SimplePlayer
from settings.screen_size import X_SCALE, Y_SCALE


# --------- SKIN SETTINGS ---------------
def reload_color():
    face_color = normalize_color((int(FACE_INPUT_R.text), int(FACE_INPUT_G.text), int(FACE_INPUT_B.text), 255))
    body_color = normalize_color((int(BODY_INPUT_R.text), int(BODY_INPUT_G.text), int(BODY_INPUT_B.text), 255))
    PLAYER_PIC.update_color(body_color=body_color, face_color=face_color)
    change_parameter_in_json_config('player_skin', {'body': body_color, 'face': face_color}, CGSJP)


__player_color = get_parameter_from_json_config('player_skin', CGSJP, def_value=PLAYERS_COLORS['blue'])
f_r, f_g, f_b = __player_color['face'][:3]
b_r, b_g, b_b = __player_color['body'][:3]
change_parameter_in_json_config('player_skin', __player_color, CGSJP)
PLAYER_PIC = SimplePlayer(1500 * X_SCALE, 100 * Y_SCALE, turn_off_camera=True, size=PLAYER_SIZE * 5,
                          player_color=__player_color, follow_mouse=1)

FACE_INPUT_R = InputElement(1250*X_SCALE, 100*Y_SCALE, text=f'{f_r}', size_x=50, size_y=40, text_active_color=GREY_RED)
FACE_INPUT_G = InputElement(1250*X_SCALE, 150*Y_SCALE, text=f'{f_g}', size_x=50, size_y=40, text_active_color=GREY_GREEN)
FACE_INPUT_B = InputElement(1250*X_SCALE, 200*Y_SCALE, text=f'{f_b}', size_x=50, size_y=40, text_active_color=GREY_BLUE)

BODY_INPUT_R = InputElement(1250*X_SCALE, 300*Y_SCALE, text=f'{b_r}', size_x=50, size_y=40, text_active_color=GREY_RED)
BODY_INPUT_G = InputElement(1250*X_SCALE, 350*Y_SCALE, text=f'{b_g}', size_x=50, size_y=40, text_active_color=GREY_GREEN)
BODY_INPUT_B = InputElement(1250*X_SCALE, 400*Y_SCALE, text=f'{b_b}', size_x=50, size_y=40, text_active_color=GREY_BLUE)

COLORS_INPUTS_LIST = [FACE_INPUT_B, FACE_INPUT_G, FACE_INPUT_R, BODY_INPUT_B, BODY_INPUT_G, BODY_INPUT_R]

COLORS_BUTTONS_DICT = {}


def add_color(inp_el):
    value = int(inp_el.text)
    value += 5
    if value > 255:
        value = 255
    inp_el.text = str(value)


def minus_color(inp_el):
    value = int(inp_el.text)
    value -= 5
    if value < 0:
        value = 0
    inp_el.text = str(value)


for color_inp in COLORS_INPUTS_LIST:
    COLORS_BUTTONS_DICT[f'{color_inp.__class__.__name__}_{color_inp.y0}'] = {
        'kwargs': {
            'x': 1200*X_SCALE,
            'y': color_inp.y0,
            'size_x': 40,
            'size_y': 40,
            'text': '-',
            'on_click_action': minus_color,
            'on_click_action_args': (color_inp,),
        }
    }

    COLORS_BUTTONS_DICT[f'{color_inp.__class__.__name__}_{color_inp._center}'] = {
        'kwargs': {
            'x': 1310*X_SCALE,
            'y': color_inp.y0,
            'size_x': 40,
            'size_y': 40,
            'text': '+',
            'on_click_action': add_color,
            'on_click_action_args': (color_inp,),
        }
    }


# ------- SOUND SETTINGS --------------
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


MUSIC_VOLUME_VALUE = Button(x=50*X_SCALE, y=100*Y_SCALE,
                            text=f'Music Volume:',
                            screen=MAIN_SCREEN,
                            border_width=0,
                            transparent=1)

VOLUME_PROGRESS_BAR = Progress_Bar(screen=MAIN_SCREEN,
                                   stage=GLOBAL_MUSIC_PLAYER.volume_stage,
                                   stages_num=GLOBAL_MUSIC_PLAYER.volume_stages,
                                   bar_pos=(300*X_SCALE, 125*Y_SCALE),
                                   bar_inner_color=GREY_DARK_2 if GLOBAL_MUSIC_PLAYER.muted else WHITE,
                                   bar_x_size=200)

MUTE_MUSIC = Button(**{
    'x': 600*X_SCALE,
    'y': 100*Y_SCALE,
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
# -------------------------------------------------------------
MAIN_MENU_SETTINGS_BUTTONS = {
    '_sound_minus': {
        'kwargs': {
            'size_x': 40,
            'size_y': 40,
            'x': 250*X_SCALE,
            'y': 100*Y_SCALE,
            'text': '-',
            'on_click_action': minus_music_volume,
        }
    },

    '_sound_add': {
        'kwargs': {
            'size_x': 40,
            'size_y': 40,
            'x': 550*X_SCALE,
            'y': 100*Y_SCALE,
            'text': '+',
            'on_click_action': add_music_volume,
        }
    },

    '_exit': {
        'kwargs': {
            'size_x': 40,
            'size_y': 40,
            'x': SCREEN_W - 55*X_SCALE,
            'y': 10*Y_SCALE,
            'text': 'X',
            'on_click_action': back_to_menu,
        }
    },

    '_set_color': {
        'kwargs': {
            'x': 1500*X_SCALE,
            'y': 300*Y_SCALE,
            'text': 'Reload color',
            'on_click_action': reload_color
        }
    }

}
MAIN_MENU_SETTINGS_BUTTONS.update(COLORS_BUTTONS_DICT)
