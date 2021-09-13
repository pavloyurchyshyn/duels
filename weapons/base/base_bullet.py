from obj_properties.base_projectile import Projectile
from obj_properties.lazy_load_mixin import PictureLazyLoadMixin
from settings.weapon_settings.base_bullet import *
from settings.game_objects_constants import *
from UI.camera import GLOBAL_CAMERA
from math import degrees
from settings.game_objects_constants import BULLETS_TYPE
from settings.game_objects_constants import SIMPLE_BULLET


class SimpleBullet(Projectile, PictureLazyLoadMixin):
    TYPE = BULLETS_TYPE
    DEFAULT_PICTURE_PATH = DEFAULT_BULLET_PICTURE
    NAME = SIMPLE_BULLET

    def __init__(self, x, y,
                 angle: float,
                 speed: float = None,
                 size: float = None,
                 owner=None,
                 damage=None,
                 **kwargs):
        size = size if size else DEFAULT_SIZE
        speed = speed if speed else DEFAULT_SPEED
        collide_shape = kwargs.get('collide_shape')

        super().__init__(x=x, y=y,
                         speed=speed,
                         angle=angle,
                         collide_shape=collide_shape,
                         **kwargs)

        self._picture = SimpleBullet.PICTURE
        self._main_screen = SimpleBullet.MAIN_SCREEN
        self._picture_rotate = SimpleBullet.ROTATE  # pygame transform.rotate

        self.size: tuple = (size, size)
        self.owner = owner
        self.draw = self.__draw if self._picture else self.__lazy_load

        self.damage = damage if damage else DEFAULT_BULLET_DAMAGE

    def update(self):
        self._update()

    def __lazy_load(self):
        self._lazy_load_picture()
        self.draw = self.__draw
        self.draw()

    def __draw(self):
        dx, dy = GLOBAL_CAMERA.camera
        x, y = self.int_position

        picture = self._picture_rotate(self._picture, -degrees(self._angle))
        self._main_screen.blit(picture, (x - picture.get_width() // 2 + dx, y - picture.get_height() // 2 + dy))

    def kill(self):
        self.stop()

    @property
    def __dict__(self):
        return {
            'x': self._position[0],
            'y': self._position[1],
            'size': self.size[0],
            'angle': self._angle,
            'speed': self._speed,
            ANGLE_CHANGE_P_SEC: self._angle_change,
            STOP_FORCE_K: self._stop_force_k,
            STOP_FORCE_VALUE: self._stop_force_value,
        }
