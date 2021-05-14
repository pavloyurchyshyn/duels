from pygame import key as KEY
from settings.default_keys import DEFAULT_GAME_KEYS, KEYS_CONFIG_FILE
import os
import json


class Keyboard:
    def __init__(self):
        if os.path.exists(KEYS_CONFIG_FILE):
            with open(KEYS_CONFIG_FILE, 'r') as k_conf:
                self._keys = json.load(k_conf)
        else:
            self._keys = DEFAULT_GAME_KEYS
            self.save()

        self._pressed = ()
        self._in_game_keyboard = dict()
        self._only_commands = []

        self.update()

        self._previous_settings = [self._keys]

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

        self._previous_settings.append(self._keys)
        self._keys[key] = new_value

        self.save()

    def save(self):
        with open(KEYS_CONFIG_FILE, 'w') as k_conf:
            json.dump(self._keys, k_conf)

    def update(self):
        self._only_commands.clear()
        self._pressed = KEY.get_pressed()

        for k in self._keys:
            if self._pressed[self._keys[k]]:
                self._in_game_keyboard[k] = 1
                self._only_commands.append(k)
            else:
                self._in_game_keyboard[k] = 0

    @property
    def commands(self):
        return self._only_commands

    @property
    def in_game_keyboard(self):
        return self._in_game_keyboard

    @property
    def pressed(self):
        return self._pressed


class KeyUsingError(Exception):
    def __init__(self, used_key):
        self.key = used_key

    def __str__(self):
        return f'Already using: {self.key}'


GLOBAL_KEYBOARD = Keyboard()
