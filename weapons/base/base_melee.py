from interfaces.simple_weapon_interface import SimpleWeaponInterface
from obj_properties.rect_form import Rectangle
from obj_properties.circle_form import Circle
from obj_properties.half_circle import HalfCircle
from math import dist
from settings.effects import OWNER_EFFECT, TARGET_EFFECT
from settings.weapon_settings.base_melee import *


class BasicMelee(Rectangle, SimpleWeaponInterface):
    def __init__(self, x, y, size_x=DEFAULT_SIZE, size_y=None,
                 hitbox_radius=DEFAULT_HITBOX_SIZE, hitbox_angles=360, **kwargs):
        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)

        self._attack_hitbox = Circle(x, y, hitbox_radius) if hitbox_angles>=360 else HalfCircle(x, y, R=hitbox_radius, hitbox_angle=hitbox_angles)
        self._hitbox_angles = hitbox_angles if hitbox_angles and 0 < hitbox_angles < 360 else None
        self._owner_effects = kwargs.get(OWNER_EFFECT, {})
        self._target_effects = kwargs.get(TARGET_EFFECT, {})
        self._owner = kwargs.get('owner')

    def attack(self):
        pass

