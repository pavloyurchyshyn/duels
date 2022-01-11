from pygame import key as KEY
from pygame import constants, locals
from settings.default_keys import DEFAULT_GAME_KEYS, KEYS_CONFIG_FILE, TEST_MESSAGE
from common_things.save_and_load_json_config import load_json_config, save_json_config
import os
from pygame.key import name as get_key_name
from pygame import KEYDOWN, KEYUP, TEXTINPUT


class Keyboard:
    def __init__(self):
        if os.path.exists(KEYS_CONFIG_FILE):
            self._keys_to_command = load_json_config(KEYS_CONFIG_FILE)
            if len(self._keys_to_command) < len(DEFAULT_GAME_KEYS):
                keys = DEFAULT_GAME_KEYS.copy()
                keys.update(self._keys_to_command)
                self._keys_to_command = keys
        else:
            self._keys_to_command = DEFAULT_GAME_KEYS
            self.save()

        self._pressed = ()
        self._in_game_keyboard = dict()
        self._only_commands = set()
        self._text = []
        self.update(())
        # start_text_input()
        self._previous_settings = [self._keys_to_command.copy()]

    def restore_default(self):
        self._keys_to_command = DEFAULT_GAME_KEYS
        self.save()

    def safety_change(self, key, new_value):
        if new_value in self._keys_to_command.values():
            key_in = None
            for k in self._keys_to_command:
                if self._keys_to_command[k] == new_value:
                    key_in = k
                    break

            raise KeyUsingError(key_in)

        else:
            self._keys_to_command[key] = new_value
            self.save()

    def back_step(self):
        if self._previous_settings:
            self._keys_to_command = self._previous_settings.pop(-1)
            self.save()

    def change(self, key, new_value):
        for k in self._keys_to_command:
            if self._keys_to_command[k] == new_value:
                self._keys_to_command[k] = None
                break

        self._previous_settings.append(self._keys_to_command.copy())
        self._keys_to_command[key] = new_value

        self.save()

    def __check_for_all_keys(self):
        for key, value in DEFAULT_GAME_KEYS.items():
            if key not in self._keys_to_command:
                self._keys_to_command[key] = value

        self.save()

    def save(self):
        save_json_config(self._keys_to_command, KEYS_CONFIG_FILE)

    def update(self, events):
        self._text.clear()
        self._pressed = KEY.get_pressed()
        for event in events:
            if event.type == KEYDOWN:
                command = self._keys_to_command.get(get_key_name(event.key))
                if command:
                    self._only_commands.add(command)
            elif event.type == KEYUP:
                command = self._keys_to_command.get(get_key_name(event.key))
                if command:
                    self._only_commands.remove(command)
            elif event.type == TEXTINPUT:
                # print(get_key_name(event.key))
                self._text.append(event.text)
        # print(self._text)

    @property
    def text(self) -> str:
        if self._text:
            return ''.join(self._text)
        else:
            return ''

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

    @property
    def test_message(self):
        return TEST_MESSAGE in self._only_commands


class KeyUsingError(Exception):
    def __init__(self, used_key):
        self.key = used_key

    def __str__(self):
        return f'Already using: {self.key}'


GLOBAL_KEYBOARD = Keyboard()
