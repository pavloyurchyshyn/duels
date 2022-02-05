from obj_properties.img_lazy_load import LoadPictureMethodLazyLoad, PygameMethodsLazyLoad, ScreenLazyLoad
from common_things.save_and_load_json_config import get_param_from_cgs
from common_things.camera import GLOBAL_CAMERA
from settings.network_settings.network_constants import PLAYER_SKIN
from settings.global_parameters import its_client_instance


class PlayerLazyLoad:
    PLAYERS_SKINS = {}
    PlayerImagesManager = None
    CIRCLE_ROT_SPEED = 0.01
    camera = GLOBAL_CAMERA

    def __init__(self, **kwargs):
        if its_client_instance():
            from player.base_visual.player_visual_part import PlayerVisualPart

            self._visual_part = PlayerVisualPart(player=self, player_size=self._size, **kwargs)
        else:
            self._visual_part = None

    def draw(self):
        raise NotImplementedError('Have to implement draw method in inheritance class')

    @property
    def int_position(self):
        return int(self._position[0]), int(self._position[1])
