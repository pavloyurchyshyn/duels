import logging
import subprocess
import os
from settings.common_settings import ROOT_OF_GAME
from settings.network_settings.network_settings import *
from settings.network_settings.network_constants import *
import time
from common_things.save_and_load_json_config import get_param_from_cgs
from _thread import start_new_thread
from common_things.loggers import LOGGER


class ServerController:
    def __init__(self):
        self._ip_address = socket.gethostbyname(socket.gethostname())
        self.port = DEFAULT_PORT
        self._server_process = None

        self.players_number = 2
        self.password = ''

    def run_server(self):
        self.update_parameters()
        arguments = self.get_arguments()
        arguments = ['python', os.path.join(ROOT_OF_GAME, SERVER_FILE_NAME), *arguments]
        LOGGER.info('Server started.')
        LOGGER.info(f'Arguments.{arguments}')
        self._server_process = subprocess.Popen(arguments)

    def stop_server(self):
        start_new_thread(self.__terminate, ())

    def __terminate(self):
        if self._server_process:
            # self._server_process.stdin.write('stop'.encode())
            # self._server_process.stdin.flush()
            time.sleep(5)
            self._server_process.terminate()
        self._server_process = None

    def get_arguments(self) -> list:
        arguments = [f'--{PORT}', str(NETWORK_DATA[PORT]),
                     f'--{PLAYERS_NUMBER}', str(NETWORK_DATA[PLAYERS_NUMBER]),
                     f'--{PASSWORD}', str(NETWORK_DATA[PASSWORD]),
                     f'--{ADMIN_AK}', str(get_param_from_cgs(NETWORK_ACCESS_KEY, def_value='None')),
                     ]

        for key, values in SERVER_ARGUMENTS.items():
            if key not in arguments:
                arguments.append(key)
                arguments.append(str(values[0]))

        return arguments

    def update_parameters(self):
        self.players_number = NETWORK_DATA[PLAYERS_NUMBER]
        self.password = NETWORK_DATA[PASSWORD]
        self.port = NETWORK_DATA[PORT]

    def __del__(self):
        self.stop_server()


SERVER_CONTROLLER = ServerController()
