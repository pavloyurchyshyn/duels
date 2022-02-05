from settings.window_settings import SCREEN_W, SCREEN_H, HALF_SCREEN_W, X_SCALE, Y_SCALE
from settings.window_settings import MAIN_SCREEN
from settings.colors import WHITE, GREY_DARK_2
from settings.screen_size import X_SCALE, Y_SCALE
from settings.global_parameters import set_fps

from common_things.sound_loader import GLOBAL_MUSIC_PLAYER
from common_things.stages import Stages
from common_things.global_keyboard import GLOBAL_KEYBOARD

from UI.UI_buttons.music_volume_progress_bar import VOLUME_PROGRESS_BAR
from UI.UI_buttons.mute_music_button import MUTE_MUSIC_BUTTON
from UI.UI_base.button_UI import Button
from UI.UI_base.text_UI import Text
from UI.UI_base.input_element_UI import InputElement
from UI.UI_controller import UI_TREE

MAIN_MENU_SETTINGS_BUTTONS = {}

SOUND_ADD_ID = 'sound_add'
SOUND_MINUS_ID = 'sound_minus'
EXIT_ID = 'exit'
RELOAD_COLOR_ID = 'change_color'

# ------- KEYBOARD SETTINGS -----------
KEYBOARD_SETTINGS_TEXT = Text('Key settings', x=HALF_SCREEN_W + HALF_SCREEN_W // 4, y=10 * Y_SCALE, font_size=30)

KEYBOARD_TEXT_DATA = {}
KEYBOARD_TEXT_OBJS = []
INPUT_ELEMENTS = []

x_pos_command = HALF_SCREEN_W + 100 * X_SCALE
x_pos_key = HALF_SCREEN_W + 100 * X_SCALE + 300 * X_SCALE
x_pos_warn = x_pos_key + 130 * X_SCALE
y_pos = 20 * Y_SCALE + KEYBOARD_SETTINGS_TEXT.size[1]
y_size = 50 * Y_SCALE
x_size = 100 * X_SCALE
y_step = 10 * Y_SCALE

COMMANDS_WHICH_USING_KEY = []

for key, command in GLOBAL_KEYBOARD.get_key_command_values():
    KEYBOARD_TEXT_DATA[command] = {'kwargs': {
        'size': (x_size, y_size),
        'x': x_pos_command,
        'y': y_pos,
        'text': command.lower().capitalize().replace('_', ' '),
        'font_size': 25,
    }}


    def on_input_action(self):
        command_ = self.id
        new_key = self._text_text if self._text_text else None

        if not new_key:
            GLOBAL_KEYBOARD.change(command=command_, new_key=new_key)
            self._text_text = None
            return

        for comm in GLOBAL_KEYBOARD.get_commands_by_key(new_key):
            if comm != command_:
                UI_TREE.get_element('main_menu_settings', comm).text = '!'

        GLOBAL_KEYBOARD.change(command=command_, new_key=new_key)
        self._text_text = new_key.upper()


    inp_el = InputElement(x=x_pos_key, y=y_pos,
                          size_x=x_size, size_y=y_size,
                          text=key.upper() if key else '_',
                          id=command,
                          on_change_action=on_input_action,
                          active_border_width=1,
                          non_active_border_width=1,
                          last_raw_input=1,
                          one_input=1,
                          default_text='!'
                          )

    INPUT_ELEMENTS.append(inp_el)

    y_pos += y_size + y_step


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

KEYBOARD_TEXT_DATA['_FPS'] = {'kwargs': {
    'size': (50, 50),
    'x': 50 * X_SCALE,
    'y': 150 * Y_SCALE,
    'text': 'FPS: ',
    'font_size': 25,
}}

SOUND_BUTTONS = {
    '_sound_minus': {
        'kwargs': {
            'size_x': 40,
            'size_y': 40,
            'x': 250 * X_SCALE,
            'y': 100 * Y_SCALE,
            'text': '-',
            'on_click_action': minus_music_volume,
            'id': SOUND_ADD_ID,
            'border_width': 1,
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
            'id': SOUND_MINUS_ID,
            'border_width': 1,

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
            'border_width': 1,

        }
    },

    '_set_fps_60': {
        'kwargs': {
            'size_x': 40,
            'size_y': 40,
            'x': 110 * X_SCALE,
            'y': 150 * Y_SCALE,
            'text': '60',
            'on_click_action': set_fps,
            'on_click_action_args': (60, ),
            'id': 'fps_60',
            'border_width': 1,

        }
    },

    '_set_fps_120': {
        'kwargs': {
            'size_x': 40,
            'size_y': 40,
            'x': 160 * X_SCALE,
            'y': 150 * Y_SCALE,
            'text': '120',
            'on_click_action': set_fps,
            'on_click_action_args': (120, ),
            'border_width': 1,

            'id': 'fps_120',
        }
    },

    '_set_fps_no_limit': {
        'kwargs': {
            'size_x': 100,
            'size_y': 40,
            'x': 210 * X_SCALE,
            'y': 150 * Y_SCALE,
            'text': 'No limit',
            'on_click_action': set_fps,
            'on_click_action_args': (0, ),
            'id': 'fps_0',
            'border_width': 1,

        }
    },
}
# -------------------------------------------------------------

MAIN_MENU_SETTINGS_BUTTONS.update(SOUND_BUTTONS)

# MAIN_MENU_SETTINGS_BUTTONS.clear()
# KEYBOARD_TEXT_DATA.clear()
# INPUT_ELEMENTS.clear()
# KEYBOARD_TEXT_OBJS.clear()