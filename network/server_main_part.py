import socket
from _thread import *
from settings.UI_setings.menus_settings.multiplayer import SERVER_PASSWORD
import subprocess
import os
from settings.common_settings import SERVER_FOLDER


class ServerController:
    def __init__(self):
        self._ip_address = socket.gethostbyname(socket.gethostname())
        self._server_process = None

    def run_server(self, players_number=2):
        arguments = self.get_arguments(players_number, passwrd=SERVER_PASSWORD.text)
        arguments = ['python', os.path.join(SERVER_FOLDER, 'server.py')]
        self._server_process = subprocess.Popen(arguments)

    def stop_server(self):
        if self._server_process:
            self._server_process.terminate()

    def get_arguments(self, players_num, passwrd) -> list:
        return []

    def __del__(self):
        self.stop_server()


SERVER_CONTROLLER = ServerController()
