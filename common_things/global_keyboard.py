from pygame import key as KEY
from pygame import constants, locals
from pygame.key import name as get_key_name
from pygame import KEYDOWN, KEYUP, TEXTINPUT
from common_things.loggers import LOGGER
from settings.default_keys import DEFAULT_COMMAND_KEY, KEYS_CONFIG_FILE, TEST_MESSAGE
from common_things.save_and_load_json_config import load_json_config, save_json_config
import os


class Keyboard:
    def __init__(self):
        if os.path.exists(KEYS_CONFIG_FILE):
            self._command_to_key: dict = load_json_config(KEYS_CONFIG_FILE)
            self._command_to_key = {k: v for k, v in self._command_to_key.items() if v}
            if len(self._command_to_key) < len(DEFAULT_COMMAND_KEY):
                keys = DEFAULT_COMMAND_KEY.copy()
                keys.update(self._command_to_key)
                self._command_to_key = keys
        else:
            self._command_to_key = DEFAULT_COMMAND_KEY

        self.save()

        self._keys_to_command = {}
        self.make_key_to_command_dict()

        self._pressed = ()
        self._only_commands = set()
        self._text = []

        self._last_raw_inp = ''

        self.update(())
        self._previous_settings = [self._keys_to_command.copy()]

    def make_key_to_command_dict(self):
        self._keys_to_command = {key: command for (command, key) in self._command_to_key.items()}
        LOGGER.info(f'Keys to command created: {self._keys_to_command}')

    def restore_default(self):
        self._command_to_key = DEFAULT_COMMAND_KEY
        LOGGER.info('Default keys restored.')
        self.make_key_to_command_dict()
        self.save()

    def safety_change(self, command, new_key):
        if new_key in self._command_to_key.values():
            for comm, key in self._command_to_key.items():
                if key == new_key and comm != command:
                    raise KeyUsingError(comm)
        else:
            self._command_to_key[command] = new_key
            self._previous_settings.append(self._keys_to_command.copy())
            self.make_key_to_command_dict()
            self.save()

    def back_step(self):
        if self._previous_settings:
            self._command_to_key = self._previous_settings.pop(-1)
            self.make_key_to_command_dict()
            self.save()

    def change(self, command, new_key):
        LOGGER.info(f'Changing command {command} to  {new_key}')
        if new_key:
            for command_, k in self._command_to_key.items():
                if k == new_key and command_ != command:
                    LOGGER.info(f'Command {command_} deleted.')
                    self._command_to_key[command_] = None
                    break

        self._previous_settings.append(self._command_to_key.copy())
        self._command_to_key[command] = new_key
        LOGGER.info(f'Command {command} changed to {self._command_to_key[command]}')

        self.make_key_to_command_dict()
        self.save()

    def save(self):
        LOGGER.info(f'New keys {self._command_to_key} saved to {KEYS_CONFIG_FILE}')
        save_json_config(self._command_to_key, KEYS_CONFIG_FILE)

    def update(self, events):
        self._text.clear()
        self._last_raw_inp = None
        self._pressed = KEY.get_pressed()
        for event in events:
            if event.type == KEYDOWN:
                command = self._keys_to_command.get(get_key_name(event.key))
                if command:
                    self._only_commands.add(command)
                self._last_raw_inp = get_key_name(event.key)

            elif event.type == KEYUP:
                command = self._keys_to_command.get(get_key_name(event.key))
                if command in self._only_commands:
                    self._only_commands.remove(command)

            elif event.type == TEXTINPUT:
                self._text.append(event.text)

    def get_commands_by_key(self, key):
        return (command for command, key_ in self._command_to_key.items() if key_ == key)

    @property
    def last_raw_text(self) -> str:
        return self._last_raw_inp

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

    def get_key_command_values(self):
        return self._keys_to_command.items()


class KeyUsingError(Exception):
    def __init__(self, used_key):
        self.key = used_key
        LOGGER.error(f'Already using: {self.key}')

    def __str__(self):
        return f'Already using: {self.key}'


GLOBAL_KEYBOARD = Keyboard()
