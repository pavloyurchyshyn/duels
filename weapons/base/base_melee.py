from interfaces.simple_weapon_interface import SimpleWeaponInterface
from obj_properties.rect_form import Rectangle
from math import dist
from interfaces.collide_interfaces import CollideInterface


class BasicMelee(Rectangle, SimpleWeaponInterface):
    def __init__(self, x, y, size_x, size_y=None, hitbox_angles=360):
        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)

        self._hitbox_angles = hitbox_angles if hitbox_angles and 0 < hitbox_angles < 360 else None


    def attack(self):
        pass


class BasicMeleeHitbox(CollideInterface):
    def __init__(self, angle=-1):
