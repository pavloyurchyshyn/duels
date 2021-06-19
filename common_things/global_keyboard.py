from pygame import key as KEY
from pygame import constants, locals
from settings.default_keys import DEFAULT_GAME_KEYS, KEYS_CONFIG_FILE
from common_things.save_and_load_json_config import load_json_config, save_json_config
import os

key_to_text = {
    constants.K_1: '1', constants.K_2: '2', constants.K_3: '3',
    constants.K_4: '4', constants.K_5: '5', constants.K_6: '6',
    constants.K_7: '7', constants.K_8: '8', constants.K_9: '9', constants.K_0: '0',

    constants.K_q: 'q', constants.K_w: 'w', constants.K_e: 'e', constants.K_r: 'r',
    constants.K_t: 't', constants.K_y: 'y', constants.K_u: 'u', constants.K_i: 'i',
    constants.K_o: 'o', constants.K_p: 'p',

    constants.K_a: 'a', constants.K_s: 's', constants.K_d: 'd', constants.K_f: 'f',
    constants.K_g: 'g', constants.K_h: 'h', constants.K_j: 'j', constants.K_k: 'k',
    constants.K_l: 'l',

    constants.K_TAB: '   ', constants.K_SPACE: ' ',

    constants.K_z: 'z', constants.K_x: 'x', constants.K_c: 'c', constants.K_v: 'v',
    constants.K_b: 'b', constants.K_n: 'n', constants.K_m: 'm', constants.K_MINUS: '-',

    constants.K_UNDERSCORE: '_',

}


class Keyboard:
    def __init__(self):
        if os.path.exists(KEYS_CONFIG_FILE):
            self._keys = load_json_config(KEYS_CONFIG_FILE)
        else:
            self._keys = DEFAULT_GAME_KEYS
            self.save()

        self._pressed = ()
        self._in_game_keyboard = dict()
        self._only_commands = set()

        self.update()

        self._previous_settings = [self._keys.copy()]

    def restore_default(self):
        self._keys = DEFAULT_GAME_KEYS
        self.save()

    def safety_change(self, key, new_value):
        if new_value in self._keys.values():
            key_in = None
            for k in self._keys:
                if self._keys[k] == new_value:
                    key_in = k
                    break

            raise KeyUsingError(key_in)

        else:
            self._keys[key] = new_value
            self.save()

    def back_step(self):
        if self._previous_settings:
            self._keys = self._previous_settings.pop(-1)
            self.save()

    def change(self, key, new_value):
        for k in self._keys:
            if self._keys[k] == new_value:
                self._keys[k] = None
                break

        self._previous_settings.append(self._keys.copy())
        self._keys[key] = new_value

        self.save()

    def __check_for_all_keys(self):
        for key, value in DEFAULT_GAME_KEYS.items():
            if key not in self._keys:
                self._keys[key] = value

        self.save()

    def save(self):
        save_json_config(self._keys, KEYS_CONFIG_FILE)

    def update(self):
        self._only_commands.clear()
        self._pressed = KEY.get_pressed()

        for k in self._keys:
            if self._pressed[self._keys[k]]:
                self._in_game_keyboard[k] = 1
                self._only_commands.add(k)
            else:
                self._in_game_keyboard[k] = 0

    @property
    def text(self) -> str:
        text = ''
        for key in key_to_text:
            if self._pressed[key]:
                text = f'{text}{key_to_text[key]}'

        if self._pressed[constants.K_LSHIFT]:
            text = text.upper()

        return text

    @property
    def commands(self):
        return self._only_commands

    @property
    def in_game_keyboard(self):
        return self._in_game_keyboard

    @property
    def pressed(self):
        return self._pressed

    @property
    def ESC(self):
        return self._pressed[constants.K_ESCAPE]

    @property
    def ENTER(self):
        return self._pressed[constants.K_RETURN]

    @property
    def BACKSPACE(self):
        return self._pressed[constants.K_BACKSPACE]


class KeyUsingError(Exception):
    def __init__(self, used_key):
        self.key = used_key

    def __str__(self):
        return f'Already using: {self.key}'


GLOBAL_KEYBOARD = Keyboard()
