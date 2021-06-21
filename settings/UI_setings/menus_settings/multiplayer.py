from settings.global_parameters import GLOBAL_SETTINGS
from settings.window_settings import SCREEN_W, MAIN_SCREEN, HALF_SCREEN_W, SCREEN_H
from settings.game_stages import CURRENT_STAGE, MAIN_MENU_S, HOST_SERVER
from settings.UI_setings.button_settings import DEFAULT_BUTTON_HALF_X_SIZE, DEFAULT_BUTTON_Y_SIZE, DEFAULT_BUTTON_X_SIZE
from settings.network_settings import DEFAULT_PORT, update_host_address
from settings.common_settings import PLAYER_NICKNAME_KEY, COMMON_GAME_SETTINGS_JSON_PATH

from UI.UI_base.input_element_UI import InputElement
from UI.UI_base.button_UI import Button
from UI.UI_base.text_UI import Text

from common_things.save_and_load_json_config import save_json_config, load_json_config, \
    get_parameter_from_json_config, change_parameter_in_json_config

import clipboard
import socket
import re

IP_REGULAR = '\b((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.|$)){4}\b'


def back_to_menu():
    GLOBAL_SETTINGS[CURRENT_STAGE] = MAIN_MENU_S


# ===== CLIENT PART ================

def anon_host(host):
    host = host.strip()
    host = host.split(':')[0]
    pre, post = host[:2], host[-2:]
    host = host[2:-2]

    for i in range(0, 10):
        host = host.replace(str(i), '*')
    host = f'{pre}{host}{post}'
    return f'{host}'


def paste_host_address():
    host = clipboard.paste()
    clipboard.copy('')
    if re.search(IP_REGULAR, host.split(':')[0]) or 1:  # ----->
        update_host_address(host)
        SERVER_ADDRESS.change_text(anon_host(host))
    else:
        pass
        # TODO Add message WRONG IP


def paste_pass():
    pswrd = clipboard.paste()
    PASSWORD_INPUT_CLIENT.text = pswrd


PASSWORD_TEXT_CLIENT = Text(x=HALF_SCREEN_W + DEFAULT_BUTTON_HALF_X_SIZE // 2,
                            y=300, text='Server password:', screen=MAIN_SCREEN)

# PASSWORD_VALUE_CLIENT = Text(x=HALF_SCREEN_W + DEFAULT_BUTTON_HALF_X_SIZE // 2,
#                              y=300, text='', screen=MAIN_SCREEN)

PASSWORD_INPUT_CLIENT = InputElement(x=HALF_SCREEN_W + DEFAULT_BUTTON_X_SIZE + 150,
                                     y=290,
                                     size_x=300,
                                     text='',
                                     default_text='Enter password')


def nick_change():
    new_nick_name = NICKNAME_INPUT.text
    if new_nick_name:
        change_parameter_in_json_config(PLAYER_NICKNAME_KEY,
                                        new_nick_name,
                                        COMMON_GAME_SETTINGS_JSON_PATH)


NICKNAME_TEXT = Text(x=HALF_SCREEN_W + DEFAULT_BUTTON_HALF_X_SIZE // 2,
                     y=110,
                     screen=MAIN_SCREEN,
                     text='Nickname:')

NICKNAME_INPUT = InputElement(x=HALF_SCREEN_W + DEFAULT_BUTTON_X_SIZE + 50,
                              y=100,
                              size_x=200,
                              text=get_parameter_from_json_config(key=PLAYER_NICKNAME_KEY,
                                                                  path=COMMON_GAME_SETTINGS_JSON_PATH,
                                                                  def_value=''),
                              on_change_action=nick_change,
                              default_text='Enter nickname')

SERVER_ADDRESS_TEXT = Text(x=HALF_SCREEN_W + DEFAULT_BUTTON_HALF_X_SIZE // 2,
                           y=200, text='Server address:', screen=MAIN_SCREEN)

SERVER_ADDRESS = Text(x=HALF_SCREEN_W + DEFAULT_BUTTON_HALF_X_SIZE + DEFAULT_BUTTON_X_SIZE,
                      y=200, text='---.---.---.---', screen=MAIN_SCREEN)

# ==== HOST PART ============
SERVER_PASSWORD = InputElement(x=50, y=100, default_text='Enter password', )


def copy_pass():
    clipboard.copy(SERVER_PASSWORD.text)


def copy_ip():
    clipboard.copy(f'{socket.gethostbyname(socket.gethostname())}:{DEFAULT_PORT}')


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
    num = int(PLAYERS_NUMBER.text)
    PLAYERS_NUMBER.change_text(str(num + 1))


def minus_player():
    num = int(PLAYERS_NUMBER.text)
    if num > 2:
        PLAYERS_NUMBER.change_text(str(num - 1))


PLAYERS_NUMBER = Text(text='2',
                      x=355,
                      y=300,
                      size=35,
                      screen=MAIN_SCREEN)

IP_VALUE = Button(x=50, y=200, size_x=250,
                  text=f'Your Address: {get_hidden_ip()}',
                  screen=MAIN_SCREEN,
                  border_width=0, transparent=1)

P_NUM = Button(x=50, y=300,
               size_x=250,
               text=f'Players number:',
               screen=MAIN_SCREEN,
               border_width=0,
               transparent=1)

MULTIPLAYER_BUTTONS = {
    # ========================== Host Part ========================
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
            'y': SCREEN_H - DEFAULT_BUTTON_Y_SIZE * 2,
            'size_x': 200,
            'text': 'RUN SEVER',
            'on_click_action': run_server,
        }
    },

    # ========================== Client Part ========================
    '_ip': {
        'kwargs': {
            'x': HALF_SCREEN_W + HALF_SCREEN_W // 2 - DEFAULT_BUTTON_HALF_X_SIZE,
            'y': SCREEN_H - DEFAULT_BUTTON_Y_SIZE * 2,
            'size_x': 200,
            'text': 'JOIN SERVER',
        }
    },

    '_paste_address': {
        'kwargs': {
            'x': HALF_SCREEN_W + DEFAULT_BUTTON_HALF_X_SIZE + 300,
            'y': 190,
            # 'size_x': 200,
            'text': 'Paste',
            'on_click_action': paste_host_address,
            # 'border_width': 0,
        }
    },

    '_paste_pswd': {
        'kwargs': {
            'x': HALF_SCREEN_W + DEFAULT_BUTTON_HALF_X_SIZE + DEFAULT_BUTTON_X_SIZE * 4,
            'y': 290,
            'on_click_action': paste_pass,
            'text': 'Paste pswrd', }
    },

}
