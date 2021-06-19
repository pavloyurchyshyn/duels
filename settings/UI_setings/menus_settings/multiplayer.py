from settings.global_parameters import GLOBAL_SETTINGS
from settings.window_settings import SCREEN_W
from settings.game_stages import MAIN_MENU_SETTINGS_S, CURRENT_STAGE, START_ROUND_S, TEST_DRAW_S, MAIN_MENU_S

from UI.UI_base.input_element_UI import InputElement
from UI.UI_base.button_UI import Button
import clipboard
import socket

SERVER_PASSWORD = InputElement(x=100, y=100, default_text='Enter password', )

BUTTONS_OBJECTS = []


def back_to_menu():
    GLOBAL_SETTINGS[CURRENT_STAGE] = MAIN_MENU_S


def copy_pass():
    clipboard.copy(SERVER_PASSWORD.text)


def reload_ip():
    SERVER_PASSWORD.text = socket.gethostbyname(socket.gethostname())


MULTIPLAYER_BUTTONS = {
    '_update_ip': {
        'kwargs': {
            'x': 100,
            'y': 250,
            'on_click_action': reload_ip,
            'text': 'Reload IP',
        }
    },

    '_copy_pswd': {
        'kwargs': {
            'x': 260,
            'y': 100,
            'on_click_action': copy_pass,
            'text': 'Copy pswrd', }
    },

    '_exit': {
        'args': (),
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
