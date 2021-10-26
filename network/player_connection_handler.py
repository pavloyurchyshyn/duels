from socket import socket
from settings.network_settings.network_settings import CONNECTION_TIMEOUT
from time import time


class ConnectionHandler:
    def __init__(self, connection: socket):
        self.connection: socket = connection
        self._last_successful_send = time()

    def send(self, data):
        try:
            self.connection.send(data)
        except Exception as e:
            if CONNECTION_TIMEOUT < time() - self._last_successful_send:
                raise TimeoutError('Connection lost')
        else:
            self._last_successful_send = time()

    def recv(self, size=2048):
        return self.connection.recv(size)

    def close(self):
        self.connection.close()
