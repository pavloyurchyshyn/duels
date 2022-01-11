from common_things.stages import Stages
from settings.window_settings import SCREEN_W
from settings.window_settings import MAIN_SCREEN
from settings.colors import WHITE, GREY_DARK_2, GREY_BLUE, GREY_RED, GREY_GREEN, PLAYERS_COLORS
from settings.players_settings.player_settings import PLAYER_SIZE
from settings.common_settings import COMMON_GAME_SETTINGS_JSON_PATH as CGSJP
from common_things.sound_loader import GLOBAL_MUSIC_PLAYER
from UI.UI_buttons.music_volume_progress_bar import VOLUME_PROGRESS_BAR
from UI.UI_buttons.mute_music_button import MUTE_MUSIC_BUTTON

from UI.UI_base.button_UI import Button
from UI.UI_base.input_element_UI import InputElement

from common_things.save_and_load_json_config import get_parameter_from_json_config, save_param_to_cgs
from common_things.img_loader import normalize_color
from player.simple_player import SimplePlayer

# from settings.screen_size import X_SCALE, Y_SCALE
X_SCALE, Y_SCALE = 1, 1

SOUND_ADD_ID = 'sound_add'
SOUND_MINUS_ID = 'sound_minus'
EXIT_ID = 'exit'
RELOAD_COLOR_ID = 'change_color'


# --------- SKIN SETTINGS ---------------
def reload_color():
    face_color = normalize_color((int(FACE_INPUT_R.text), int(FACE_INPUT_G.text), int(FACE_INPUT_B.text), 255))
    body_color = normalize_color((int(BODY_INPUT_R.text), int(BODY_INPUT_G.text), int(BODY_INPUT_B.text), 255))
    PLAYER_PIC.update_color(body_color=body_color, face_color=face_color)
    save_param_to_cgs('player_skin', {'body': tuple(body_color), 'face': tuple(face_color)})


__player_color = get_parameter_from_json_config('player_skin', CGSJP, def_value=PLAYERS_COLORS['blue'])
f_r, f_g, f_b = __player_color['face'][:3]
b_r, b_g, b_b = __player_color['body'][:3]
save_param_to_cgs('player_skin', __player_color)
PLAYER_PIC = SimplePlayer(1500 * X_SCALE, 200 * Y_SCALE, turn_off_camera=True,
                          size=PLAYER_SIZE * 5, add_self_to_list=0,
                          player_color=__player_color, follow_mouse=1,
                          draw_health_points=False, arena=None)

FACE_INPUT_R = InputElement(1250 * X_SCALE, 100 * Y_SCALE, text=f'{f_r}', size_x=50, size_y=40,
                            text_active_color=GREY_RED, id='face_inp_r')
FACE_INPUT_G = InputElement(1250 * X_SCALE, 150 * Y_SCALE, text=f'{f_g}', size_x=50, size_y=40,
                            text_active_color=GREY_GREEN, id='face_inp_g')
FACE_INPUT_B = InputElement(1250 * X_SCALE, 200 * Y_SCALE, text=f'{f_b}', size_x=50, size_y=40,
                            text_active_color=GREY_BLUE, id='face_inp_b')

BODY_INPUT_R = InputElement(1250 * X_SCALE, 300 * Y_SCALE, text=f'{b_r}', size_x=50, size_y=40,
                            text_active_color=GREY_RED, id='body_inp_r')
BODY_INPUT_G = InputElement(1250 * X_SCALE, 350 * Y_SCALE, text=f'{b_g}', size_x=50, size_y=40,
                            text_active_color=GREY_GREEN, id='body_inp_g')
BODY_INPUT_B = InputElement(1250 * X_SCALE, 400 * Y_SCALE, text=f'{b_b}', size_x=50, size_y=40,
                            text_active_color=GREY_BLUE, id='body_inp_b')

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
            'x': 1200 * X_SCALE,
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
            'x': 1310 * X_SCALE,
            'y': color_inp.y0,
            'size_x': 40,
            'size_y': 40,
            'text': '+',
            'on_click_action': add_color,
            'on_click_action_args': (color_inp,),
        }
    }


# ------- SOUND SETTINGS --------------

def minus_music_volume():
    GLOBAL_MUSIC_PLAYER.minus_volume()
    VOLUME_PROGRESS_BAR.update(current_stage=GLOBAL_MUSIC_PLAYER.volume_stage,
                               bar_color=WHITE if not GLOBAL_MUSIC_PLAYER.muted else GREY_DARK_2)


def add_music_volume():
    GLOBAL_MUSIC_PLAYER.add_volume()
    VOLUME_PROGRESS_BAR.update(current_stage=GLOBAL_MUSIC_PLAYER.volume_stage,
                               bar_color=WHITE)
    MUTE_MUSIC_BUTTON.change_picture(active=1)


MUSIC_VOLUME_VALUE = Button(x=50 * X_SCALE, y=100 * Y_SCALE,
                            text=f'Music Volume:',
                            screen=MAIN_SCREEN,
                            border_width=0,
                            transparent=1)

# -------------------------------------------------------------


MAIN_MENU_SETTINGS_BUTTONS = {
    '_sound_minus': {
        'kwargs': {
            'size_x': 40,
            'size_y': 40,
            'x': 250 * X_SCALE,
            'y': 100 * Y_SCALE,
            'text': '-',
            'on_click_action': minus_music_volume,
            'id': SOUND_ADD_ID,
        }
    },

    '_sound_add': {
        'kwargs': {
            'size_x': 40,
            'size_y': 40,
            'x': 550 * X_SCALE,
            'y': 100 * Y_SCALE,
            'text': '+',
            'on_click_action': add_music_volume,
            'id': SOUND_MINUS_ID
        }
    },

    '_exit': {
        'kwargs': {
            'size_x': 40,
            'size_y': 40,
            'x': SCREEN_W - 55 * X_SCALE,
            'y': 10 * Y_SCALE,
            'text': 'X',
            'on_click_action': Stages().set_main_menu_stage,
            'id': EXIT_ID,
        }
    },

    '_set_color': {
        'kwargs': {
            'x': 1500 * X_SCALE,
            'y': 300 * Y_SCALE,
            'text': 'Reload color',
            'on_click_action': reload_color,
            'id': RELOAD_COLOR_ID
        }
    }

}
MAIN_MENU_SETTINGS_BUTTONS.update(COLORS_BUTTONS_DICT)
