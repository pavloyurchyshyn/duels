import socket
import pickle
import json

from settings.network_settings import NETWORK_DATA, anon_host, DEFAULT_PORT
from settings.network_settings import IP, NICKNAME, PASSWORD, PORT
from common_things.loggers import LOGGER

from common_things.save_and_load_json_config import get_parameter_from_json_config, change_parameter_in_json_config
from settings.common_settings import COMMON_GAME_SETTINGS_JSON_PATH as CGSJP


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

        self._network_address_key = get_parameter_from_json_config('network_address_key', CGSJP, def_value=None)

    def update_network_data(self):
        self.server = NETWORK_DATA[IP]
        self.port = NETWORK_DATA[PORT]
        self.nickname = NETWORK_DATA[NICKNAME]
        self.password = NETWORK_DATA[PASSWORD]
        self.addr = (self.server, self.port)

        self.credentials.clear()
        self.credentials[NICKNAME] = self.nickname
        self.credentials[PASSWORD] = self.password
        self.credentials['player_color'] = get_parameter_from_json_config('player_skin', CGSJP, def_value='blue')
        self.credentials['network_address_key'] = get_parameter_from_json_config('network_address_key', CGSJP, def_value=self._network_address_key)

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
                change_parameter_in_json_config(response.get('network_address_key'), 'network_address_key', CGSJP)
                self._network_address_key = response.get('network_address_key')
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
