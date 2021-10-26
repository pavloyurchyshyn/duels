from settings.global_parameters import GLOBAL_SETTINGS
from settings.window_settings import SCREEN_W, MAIN_SCREEN, HALF_SCREEN_W, SCREEN_H
from settings.game_stages_constants import CURRENT_STAGE, MAIN_MENU_STAGE, HOST_SERVER_STAGE, MULTIPLAYER_CLIENT_CONNECT_ROUND_STAGE
from settings.UI_setings.button_settings import DEFAULT_BUTTON_HALF_X_SIZE, DEFAULT_BUTTON_Y_SIZE, DEFAULT_BUTTON_X_SIZE
from settings.network_settings.network_settings import DEFAULT_PORT, update_host_address, NETWORK_DATA, anon_host, IP, PASSWORD
from settings.common_settings import PLAYER_NICKNAME_KEY, COMMON_GAME_SETTINGS_JSON_PATH
#from settings.screen_size import X_SCALE, Y_SCALE
X_SCALE, Y_SCALE = 1, 1

from UI.UI_base.input_element_UI import InputElement
from UI.UI_base.button_UI import Button
from UI.UI_base.text_UI import Text

from common_things.save_and_load_json_config import save_json_config, load_json_config, \
    get_parameter_from_json_config, change_parameter_in_json_config

import clipboard
import socket
import re
import base64

IP_REGULAR = r'(\d{1,3}\.){3}\d\d?\d?:(\d{4,5})'


def back_to_menu():
    GLOBAL_SETTINGS[CURRENT_STAGE] = MAIN_MENU_STAGE


# ===== CLIENT PART ================

def connect_as_client():
    if NETWORK_DATA[IP]:
        GLOBAL_SETTINGS[CURRENT_STAGE] = MULTIPLAYER_CLIENT_CONNECT_ROUND_STAGE
    else:
        # TODO ERROR MESSAGE
        pass


def paste_host_address():
    host = clipboard.paste()
    if re.search(r"b'.*'", host):
        host = host.replace('b', '').replace("'", '')
        host = base64.b64decode(host).decode()
        if re.search(IP_REGULAR, host):  # ----->
            update_host_address(host)
            SERVER_ADDRESS.change_text(anon_host(host))
        else:
            pass
            # TODO Add message WRONG IP
    else:
        # TODO Add message WRONG IP
        pass


def paste_pass():
    pswrd = clipboard.paste()
    PASSWORD_INPUT_CLIENT.text = pswrd
    NETWORK_DATA['password'] = pswrd


def enter_pass():
    NETWORK_DATA['password'] = PASSWORD_INPUT_CLIENT.text if PASSWORD_INPUT_CLIENT.text else '.'


PASSWORD_TEXT_CLIENT = Text(x=HALF_SCREEN_W + DEFAULT_BUTTON_HALF_X_SIZE // 2,
                            y=300*Y_SCALE, text='Server password:', screen=MAIN_SCREEN)

PASSWORD_TEXT_HOST = Text(x=SCREEN_W * 0.02632,
                          y=SCREEN_H * 0.1018, text='Server password:', screen=MAIN_SCREEN)

PASSWORD_INPUT_CLIENT = InputElement(x=HALF_SCREEN_W + DEFAULT_BUTTON_X_SIZE + 300//2,
                                     y=int(SCREEN_H * 0.2685),
                                     size_x=300,
                                     text='',
                                     on_change_action=enter_pass,
                                     default_text='Enter password')


def nick_change():
    new_nick_name = NICKNAME_INPUT.text
    NETWORK_DATA['nickname'] = new_nick_name
    if new_nick_name:
        change_parameter_in_json_config(PLAYER_NICKNAME_KEY,
                                        new_nick_name,
                                        COMMON_GAME_SETTINGS_JSON_PATH)


NICKNAME_TEXT = Text(x=HALF_SCREEN_W + DEFAULT_BUTTON_HALF_X_SIZE // 2,
                     y=110*Y_SCALE,
                     screen=MAIN_SCREEN,
                     text='Nickname:')

NICKNAME_INPUT = InputElement(x=HALF_SCREEN_W + DEFAULT_BUTTON_X_SIZE + int(50*Y_SCALE),
                              y=int(SCREEN_H * 0.09259),
                              size_x=200,
                              text=get_parameter_from_json_config(key=PLAYER_NICKNAME_KEY,
                                                                  path=COMMON_GAME_SETTINGS_JSON_PATH,
                                                                  def_value=''),
                              on_change_action=nick_change,
                              default_text='Enter nickname')

SERVER_ADDRESS_TEXT = Text(x=HALF_SCREEN_W + DEFAULT_BUTTON_HALF_X_SIZE // 2,
                           y=SCREEN_H * 0.18518, text='Server address:', screen=MAIN_SCREEN)

SERVER_ADDRESS = Text(x=HALF_SCREEN_W + DEFAULT_BUTTON_HALF_X_SIZE + DEFAULT_BUTTON_X_SIZE,
                      y=SCREEN_H * 0.18518, text='l.o.c.a.l.h.o.s.t', screen=MAIN_SCREEN)


# ==== HOST PART ============
def password_change():
    NETWORK_DATA[PASSWORD] = SERVER_PASSWORD.text if SERVER_PASSWORD.text else '.'


SERVER_PASSWORD = InputElement(x=250*X_SCALE, y=100*Y_SCALE, default_text='Enter password', on_change_action=password_change)


def copy_pass():
    clipboard.copy(SERVER_PASSWORD.text)


def copy_ip():
    address = f'{socket.gethostbyname(socket.gethostname())}:{DEFAULT_PORT}'
    address = str(base64.b64encode(address.encode()))
    clipboard.copy(address)


def run_server():
    GLOBAL_SETTINGS[CURRENT_STAGE] = HOST_SERVER_STAGE


def reload_ip():
    IP_VALUE.text = f'Your Address: {anon_host(socket.gethostbyname(socket.gethostname()))}'


def add_player():
    num = NETWORK_DATA['players_number']
    PLAYERS_NUMBER.change_text(str(num + 1))
    NETWORK_DATA['players_number'] = num + 1


def minus_player():
    num = NETWORK_DATA['players_number']
    if num > 2:
        PLAYERS_NUMBER.change_text(str(num - 1))
        NETWORK_DATA['players_number'] = num - 1


PLAYERS_NUMBER = Text(text=NETWORK_DATA['players_number'],
                      x=355*X_SCALE,
                      y=300*Y_SCALE,
                      size=35,
                      screen=MAIN_SCREEN)

IP_VALUE = Button(x=50*X_SCALE, y=200*Y_SCALE, size_x=250,
                  text=f'Your Address: {anon_host(socket.gethostbyname(socket.gethostname()))}',
                  screen=MAIN_SCREEN,
                  border_width=0, transparent=1)

P_NUM = Button(x=50*X_SCALE, y=300*Y_SCALE,
               size_x=250,
               text=f'Players number:',
               screen=MAIN_SCREEN,
               border_width=0,
               transparent=1)

MULTIPLAYER_BUTTONS = {
    # ========================== Host Part ========================
    '_update_ip': {
        'kwargs': {
            'x': 310*X_SCALE,
            'y': 200*Y_SCALE,
            'on_click_action': reload_ip,
            'text': 'Reload IP',
        }
    },

    '_add_player': {
        'kwargs': {
            'x': 400*X_SCALE,
            'y': 300*Y_SCALE,
            'size_x': 40,
            'size_y': 40,
            'text': '+',
            'on_click_action': add_player,
        }
    },
    '_minus_player': {
        'kwargs': {
            'x': 300*X_SCALE,
            'y': 300*Y_SCALE,
            'size_x': 40,
            'size_y': 40,
            'text': '-',
            'on_click_action': minus_player,
        }
    },

    '_copy_ip': {
        'kwargs': {
            'x': 470*X_SCALE,
            'y': 200*Y_SCALE,
            'on_click_action': copy_ip,
            'text': 'Copy IP',
        }
    },

    '_copy_pswd': {
        'kwargs': {
            'x': 410*X_SCALE,
            'y': 100*Y_SCALE,
            'on_click_action': copy_pass,
            'text': 'Copy pswrd', }
    },

    '_exit': {
        'args': (),
        'kwargs': {
            'size_x': 40,
            'size_y': 40,
            'x': SCREEN_W - 55*X_SCALE,
            'y': 10*Y_SCALE,
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
            'on_click_action': connect_as_client,
        }
    },

    '_paste_address': {
        'kwargs': {
            'x': HALF_SCREEN_W + DEFAULT_BUTTON_HALF_X_SIZE + 300,
            'y': 190*Y_SCALE,
            # 'size_x': 200,
            'text': 'Paste',
            'on_click_action': paste_host_address,
            # 'border_width': 0,
        }
    },

    '_paste_pswd': {
        'kwargs': {
            'x': HALF_SCREEN_W + DEFAULT_BUTTON_HALF_X_SIZE + DEFAULT_BUTTON_X_SIZE * 4,
            'y': 290*Y_SCALE,
            'on_click_action': paste_pass,
            'text': 'Paste pswrd', }
    },

}
