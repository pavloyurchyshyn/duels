import socket
import json

from settings.network_settings.network_settings import NETWORK_DATA, DEFAULT_PORT
from settings.network_settings.network_constants import IP, NICKNAME, PASSWORD, PORT, NETWORK_ACCESS_KEY, PLAYER_SKIN
from common_things.loggers import LOGGER

from common_things.save_and_load_json_config import save_param_to_cgs, get_param_from_cgs


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

        self._network_access_key = get_param_from_cgs(NETWORK_ACCESS_KEY, def_value=None)

    def update_network_data(self):
        self.server = NETWORK_DATA[IP]
        self.port = NETWORK_DATA[PORT]
        self.nickname = NETWORK_DATA[NICKNAME]
        self.password = NETWORK_DATA[PASSWORD]
        self.addr = (self.server, self.port)

        self.credentials.clear()
        self.credentials[NICKNAME] = self.nickname
        self.credentials[PASSWORD] = self.password
        self.credentials[PLAYER_SKIN] = get_param_from_cgs('player_skin', def_value='blue')
        self.credentials[NETWORK_ACCESS_KEY] = get_param_from_cgs(NETWORK_ACCESS_KEY, def_value=self._network_access_key)

    def connect(self):
        self.client.close()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.update_network_data()

        try:
            self.client.connect(self.addr)
            self.client.send(self.json_to_str(self.credentials))
            response = self.str_to_json(self.client.recv(2048).decode())
            if response.get('connected'):
                self.connected = True
                save_param_to_cgs(key=NETWORK_ACCESS_KEY, value=response.get(NETWORK_ACCESS_KEY))
                self._network_access_key = response.get(NETWORK_ACCESS_KEY)
                return response
            else:
                self.disconnect()
                return response

        except Exception as e:
            self.disconnect()
            return {'connected': False, 'server_msg': f'{e}'}

    def disconnect(self):
        try:
            self.client.close()
        except:
            pass
        finally:
            self.connected = False

    @staticmethod
    def str_to_json(string):
        # print(string)
        try:
            if string:
                return json.loads(string)
            else:
                return {}
        except Exception as e:
            LOGGER.error(f'Failed to convert {string} to json: {e}')
            # print(string)
            return {}

    @staticmethod
    def json_to_str(json_):
        return json.dumps(json_).encode()

    def send(self, data):
        try:
            self.client.send(data)
        except socket.error as e:
            LOGGER.error(f"Failed to send data {e}")

    def receive(self):
        # try:
        return self.client.recv(2048).decode()
        # except Exception as e:
        #     LOGGER.error(e)

    def get_data(self):
        # try:
        data = self.receive()
        # print(data)
        return self.str_to_json(data)
        # except Exception as e:
        #     LOGGER.error(f"Failed to get data {e}")

    def update(self, data):
        self.send(self.json_to_str(data))

        return self.get_data()

    def __del__(self):
        self.disconnect()
