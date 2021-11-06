from common_things.singletone import Singleton
from settings.game_stages_constants import *
from settings.global_parameters import GLOBAL_SETTINGS


class Stages(metaclass=Singleton):
    def __init__(self):
        self.current_stage = 'main_menu'

    def get_current_stage(self) -> str:
        return self.current_stage

    def current_stage_is_menu(self) -> bool:
        return self.get_current_stage() in MENUS_STAGES_LISTS

    def change_current_stage(self, stage):
        self.current_stage = stage

    def set_host_server_stage(self):
        self.change_current_stage(HOST_SERVER_STAGE)

    def set_multiplayer_client_connect_round_stage(self):
        self.change_current_stage(MULTIPLAYER_CLIENT_CONNECT_ROUND_STAGE)

    def set_start_round_stage(self) -> None:
        self.change_current_stage(START_ROUND_STAGE)

    def set_round_stage(self) -> None:
        self.change_current_stage(ROUND_STAGE)

    def set_round_pause_stage(self) -> None:
        self.change_current_stage(ROUND_PAUSE_STAGE)

    def set_main_menu_stage(self) -> None:
        self.change_current_stage(MAIN_MENU_STAGE)

    def set_loading_stage(self) -> None:
        self.change_current_stage(LOADING_STAGE)

    def set_main_menu_settings_stage(self) -> None:
        self.change_current_stage(MAIN_MENU_SETTINGS_STAGE)

    def set_multiplayer_menu_stage(self) -> None:
        self.change_current_stage(MULTIPLAYER_MENU_STAGE)

    def set_multiplayers_round_stage(self) -> None:
        self.change_current_stage(MULTIPLAYER_CLIENT_ROUND_STAGE)

    def set_multiplayers_round_pause_stage(self) -> None:
        self.change_current_stage(MULTIPLAYER_CLIENT_ROUND_PAUSE_STAGE)

    def set_multiplayers_disconnect_stage(self) -> None:
        self.change_current_stage(MULTIPLAYER_CLIENT_DISCONNECT_STAGE)

    def set_exit_stage(self) -> None:
        self.change_current_stage(EXIT_STAGE)
