from common_things.global_clock import GLOBAL_CLOCK
from obj_properties.circle_form import Circle
from settings.weapon_settings.base_range import *
from weapons.base.base_bullet import SimpleBullet

class BaseRange(Circle):
    DEFAULT_COOLDOWN = DEFAULT_COOLDOWN
    DEFAULT_PICTURE_PATH = DEFAULT_PICTURE_PLACE
    DEFAULT_SIZE = DEFAULT_SIZE

    def __init__(self, x, y, owner = None, size=None, bullet=SimpleBullet):
        size = size if size else BaseRange.DEFAULT_SIZE
        super(BaseRange, self).__init__(x=x, y=y, R=size)
        self.dt = 0
        self.owner = owner
        self.shoot_cooldown = self.DEFAULT_COOLDOWN
        self.cooldown = -1
        self._use = 0

        self._angle = 0
        self._bullet = bullet


    def update(self, angle, position):
        self.dt = GLOBAL_CLOCK.d_time
        if self.cooldown > 0:
            self.cooldown -= self.dt

        self._angle = angle
        self._change_position(position)

    def shoot(self):

    def use(self):
        if self.cooldown < 0:
            self.cooldown = self.shoot_cooldown
            self.shoot()