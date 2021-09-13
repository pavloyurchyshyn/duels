from socket import socket
from settings.network_settings.network_settings import CONNECTION_TIMEOUT
from common_things.global_clock import ROUND_CLOCK


class ConnectionHandler:
    def __init__(self, connection: socket):
        self.connection: socket = connection
        self._timeout = 0

    def send(self, data):
        try:
            self.connection.send(data)
        except Exception as e:
            self._timeout += ROUND_CLOCK.d_time
            if CONNECTION_TIMEOUT < self._timeout:
                raise TimeoutError('Connection lost')
        else:
            self._timeout = 0

    def recv(self, size=2048):
        return self.connection.recv(size)

    def close(self):
        self.connection.close()
