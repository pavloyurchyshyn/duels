from abc import abstractmethod
from settings.global_parameters import its_client_instance
from settings.spells_settings.spells_constants import BASE_ICON, BASE_ICON_SIZE
from interfaces.simple_weapon_interface import SimpleWeaponInterface


class BaseWeapon(SimpleWeaponInterface):
    ICON_PATH = BASE_ICON
    ICON = None

    def __init__(self):
        if its_client_instance() and self.ICON is None:
            if self.ICON_PATH:
                from common_things.img_loader import load_image
                self.ICON = load_image(self.ICON_PATH, size=BASE_ICON_SIZE)

    @property
    def on_cooldown(self):
        return self.cooldown < 0

