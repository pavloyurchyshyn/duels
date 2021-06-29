import socket
import pickle
import json

from settings.network_settings import NETWORK_DATA, anon_host, DEFAULT_PORT
from settings.network_settings import IP, NICKNAME, PASSWORD, PORT


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ""
        self.port = DEFAULT_PORT
        self.addr = (self.server, self.port)
        self.password = ''
        self.nickname = ''
        self.connected = False
        self.credentials = {}

    def update_network_data(self):
        self.server = NETWORK_DATA[IP]
        self.port = NETWORK_DATA[PORT]
        self.nickname = NETWORK_DATA[NICKNAME]
        self.password = NETWORK_DATA[PASSWORD]
        self.addr = (self.server, self.port)

        self.credentials.clear()
        self.credentials[NICKNAME] = self.nickname
        self.credentials[PASSWORD] = self.password

    def confirm_password(self):
        self.send(data=self.password)

    def connect(self):
        self.client.close()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.update_network_data()
        try:
            self.client.connect(self.addr)
            self.client.send(str(self.credentials).replace("\'", "\"").encode())
            response = self.client.recv(2048).decode()
            # print(response)
            if 'Connected' in response:
                self.connected = True
                return response
            else:
                self.client.close()
                self.connected = False
                raise Exception(f'Failed to connect: {anon_host(self.addr)}')
        except Exception as e:
            self.client.close()
            self.connected = False
            raise Exception(f'Failed to connect: {anon_host(self.addr)} \n\t {e}')

    def disconnect(self):
        try:
            self.client.close()
        except:
            pass
        finally:
            self.connected = False

    def send(self, data):
        try:
            self.client.send(data.encode())
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(data)
            print(e)

    def __del__(self):
        self.disconnect()
