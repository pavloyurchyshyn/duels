from common_things.camera import GLOBAL_CAMERA

from player.base.base_player import BasePlayer

from obj_properties.img_lazy_load import OnePictureLazyLoad, AdditionalLazyLoad

from settings.weapon_settings.base_range import *
from object_controller import AllObjectsController

from weapons.base.base_bullet import SimpleBullet
from math import degrees
from weapons.base.base_weapon import BaseWeapon


class BaseRange(BaseWeapon, OnePictureLazyLoad, AdditionalLazyLoad):
    obj_controller = AllObjectsController()

    PICTURE_PATH = DEFAULT_PICTURE_PLACE
    DEFAULT_SIZE = DEFAULT_SIZE
    SHOOT_EFFECT = None
    DEFAULT_COOLDOWN = DEFAULT_COOLDOWN

    def __init__(self, x, y, owner, size=None, bullet: str = SimpleBullet.OBJ_NAME):
        size = size if size else BaseRange.DEFAULT_SIZE
        OnePictureLazyLoad.__init__(self, (size, size))
        BaseWeapon.__init__(self)
        AdditionalLazyLoad.__init__(self)

        self._center = [x, y]

        self._picture = BaseRange.PICTURE.copy()
        self._main_screen = BaseRange.MAIN_SCREEN
        self._picture_rotate = BaseRange.ROTATE  # pygame transform.rotate

        self.dt = 0
        self.owner: BasePlayer = owner
        self.shoot_cooldown = self.DEFAULT_COOLDOWN
        self.cooldown = 1
        self._use = 0

        self._angle = 0
        self._bullet_type: str = bullet if bullet else SimpleBullet.OBJ_NAME
        self._arena = owner._arena

    def update(self, angle, position):
        if self.cooldown < 0:
            self.cooldown += self.owner._d_time

        self._angle = angle
        self._center = position

    def shoot(self):
        if self.SHOOT_EFFECT:
            self.SHOOT_EFFECT(*self._center, angle=self._angle, arena=self._arena)

        self.obj_controller.add_object(dict(name=self._bullet_type,
                                            data={
                                                'x': self._center[0],
                                                'y': self._center[1],
                                                'angle': self._angle,
                                                'owner': self.owner._unique_id,
                                            }))

    def use(self):
        if self.cooldown > 0:
            self.cooldown = self.shoot_cooldown
            self.shoot()

    def alt_use(self):
        pass

    def draw(self):
        dx, dy = GLOBAL_CAMERA.camera
        m_screen = self.MAIN_SCREEN
        x0, y0 = self._center

        picture = self.ROTATE(self._picture, -degrees(self._angle))
        m_screen.blit(picture, (x0 + dx - picture.get_width() // 2, y0 + dy - picture.get_height() // 2))

    def additional_lazy_load(self):
        from visual.simple_shoot_effect import ShootEffect

        BaseRange.SHOOT_EFFECT = ShootEffect

    @property
    def size(self):
        return self.DEFAULT_SIZE, self.DEFAULT_SIZE
