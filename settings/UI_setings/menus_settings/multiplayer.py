from settings.global_parameters import GLOBAL_SETTINGS
from settings.window_settings import SCREEN_W, MAIN_SCREEN, HALF_SCREEN_W, SCREEN_H
from settings.game_stages import CURRENT_STAGE, MAIN_MENU_S, HOST_SERVER
from settings.UI_setings.button_settings import DEFAULT_BUTTON_HALF_X_SIZE, DEFAULT_BUTTON_Y_SIZE

from UI.UI_base.input_element_UI import InputElement
from UI.UI_base.button_UI import Button
from UI.UI_base.text_UI import Text
import clipboard
import socket

SERVER_PASSWORD = InputElement(x=50, y=100, default_text='Enter password', )


def back_to_menu():
    GLOBAL_SETTINGS[CURRENT_STAGE] = MAIN_MENU_S


def copy_pass():
    clipboard.copy(SERVER_PASSWORD.text)


def copy_ip():
    clipboard.copy(socket.gethostbyname(socket.gethostname()))


def run_server():
    GLOBAL_SETTINGS[CURRENT_STAGE] = HOST_SERVER


def get_hidden_ip():
    hidden_ip = socket.gethostbyname(socket.gethostname())
    for i in range(10):
        hidden_ip = hidden_ip.replace(str(i), '*')

    return hidden_ip


def reload_ip():
    IP_VALUE.text = f'Your Address: {get_hidden_ip()}'


def add_player():
    num = int(PLAYER_NUMBER.text)
    print(num)
    PLAYER_NUMBER.text = str(num + 1)


def minus_player():
    num = int(PLAYER_NUMBER.text)
    if num > 2:
        PLAYER_NUMBER.text = str(num - 1)


PLAYER_NUMBER = Button(x=350, y=300,
                       size_x=50,
                       size_y=50,
                       text='2',
                       screen=MAIN_SCREEN,
                       border_width=0,
                       transparent=1)

IP_VALUE = Button(x=50, y=200,
                  size_x=250,
                  text=f'Your Address: {get_hidden_ip()}',
                  screen=MAIN_SCREEN,
                  border_width=0,
                  transparent=1)

P_NUM = Button(x=50, y=300,
               size_x=250,
               text=f'Players number:',
               screen=MAIN_SCREEN,
               border_width=0,
               transparent=1)

MULTIPLAYER_BUTTONS = {
    '_update_ip': {
        'kwargs': {
            'x': 310,
            'y': 200,
            'on_click_action': reload_ip,
            'text': 'Reload IP',
        }
    },

    '_add_player': {
        'kwargs': {
            'x': 400,
            'y': 300,
            'size_x': 40,
            'size_y': 40,
            'text': '+',
            'on_click_action': add_player,
        }
    },
    '_minus_player': {
        'kwargs': {
            'x': 300,
            'y': 300,
            'size_x': 40,
            'size_y': 40,
            'text': '-',
            'on_click_action': minus_player,
        }
    },

    '_copy_ip': {
        'kwargs': {
            'x': 470,
            'y': 200,
            'on_click_action': copy_ip,
            'text': 'Copy IP',
        }
    },

    '_copy_pswd': {
        'kwargs': {
            'x': 210,
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

    '_host': {
        'kwargs': {
            'x': HALF_SCREEN_W // 2 - DEFAULT_BUTTON_HALF_X_SIZE,
            'y': SCREEN_H - DEFAULT_BUTTON_Y_SIZE - DEFAULT_BUTTON_HALF_X_SIZE,
            'text': 'RUN SEVER',
            'on_click_action': run_server,
        }
    }

}
