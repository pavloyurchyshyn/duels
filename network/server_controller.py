import socket
import logging
import subprocess
import os
from settings.common_settings import SERVER_FOLDER
from settings.network_settings import NETWORK_DATA, DEFAULT_PORT


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
        arguments = ['python', os.path.join(SERVER_FOLDER, 'server.py'), *arguments]
        logging.info('Server started.')
        logging.info(f'Arguments.{arguments}')
        self._server_process = subprocess.Popen(arguments)

    def stop_server(self):
        if self._server_process:
            self._server_process.terminate()
        self._server_process = None

    def get_arguments(self) -> list:
        return ['--port', str(NETWORK_DATA['port']),
                '--pnum', str(NETWORK_DATA['players_number']),
                '--password', str(NETWORK_DATA['password'])]

    def update_parameters(self):
        self.players_number = NETWORK_DATA['players_number']
        self.password = NETWORK_DATA['password']
        self.port = NETWORK_DATA['port']

    def __del__(self):
        self.stop_server()


SERVER_CONTROLLER = ServerController()
