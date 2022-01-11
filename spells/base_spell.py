from common_things.common_objects_lists_dicts import SPELLS_LIST, PLAYERS_LIST, OBJECTS_LIST
from settings.global_parameters import its_client_instance
from settings.spells_settings.spells_constants import BASE_ICON, BASE_ICON_SIZE


class SpellIcon:
    ICON_PATH = BASE_ICON
    ICON = None

    def __init__(self):
        if its_client_instance() and self.ICON is None:
            if self.ICON_PATH:
                from common_things.img_loader import load_image
                self.ICON = load_image(self.ICON_PATH, size=BASE_ICON_SIZE)


class BaseSpellProjectile:
    def __init__(self):
        self._alive = 1
        SPELLS_LIST.append(self)

    def check_for_players_intersection(self):
        for player in PLAYERS_LIST:
            if player.collide(self) and player != self.owner:
                self.interact_with_player(player)

    def check_for_objects_intersection(self):
        for obj in OBJECTS_LIST:
            if obj.collide(self):
                self.interact_with_object(obj)

    def interact_with_object(self, obj):
        raise NotImplementedError("Implement this method!")

    def interact_with_player(self, player):
        raise NotImplementedError("Implement this method!")

    @property
    def alive(self):
        return self._alive

    @property
    def dead(self):
        return not self._alive
