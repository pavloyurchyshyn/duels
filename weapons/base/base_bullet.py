from obj_properties.base_projectile import Projectile
from obj_properties.lazy_load_mixin import PictureLazyLoadMixin
from settings.weapon_settings.base_bullet import *
from common_things.camera import GLOBAL_CAMERA
from math import degrees, cos, sin
from settings.weapon_settings.types_and_names import BULLETS_TYPE, SIMPLE_BULLET
from settings.game_objects_constants import ANGLE_CHANGE_P_SEC, STOP_FORCE_K, STOP_FORCE_VALUE
from settings.all_types_and_names import add_type_and_name_to_collectors


class SimpleBullet(Projectile, PictureLazyLoadMixin):
    TYPE = BULLETS_TYPE
    PICTURE_PATH = DEFAULT_BULLET_PICTURE
    NAME = SIMPLE_BULLET
    add_type_and_name_to_collectors(TYPE, NAME)

    CREATION_EFFECT = None
    DEATH_EFFECT = None
    HIT_EFFECT = None

    def __init__(self, x, y,
                 angle: float,
                 speed: float = None,
                 size: float = None,
                 owner=None,
                 damage=None,
                 push_force=150,
                 **kwargs):
        size = size if size else DEFAULT_SIZE
        self.size: tuple = (size, size)

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
        PictureLazyLoadMixin.__init__(self)
        self.owner = owner

        self.damage = damage if damage else DEFAULT_BULLET_DAMAGE
        self._push_force = push_force

        self.make_creation_effect()

    def make_death_effect(self):
        if self.DEATH_EFFECT:
            self.EFFECTS_CON.add_effect(self.DEATH_EFFECT(*self._position, angle=self._angle))

    def make_hit_effect(self):
        if self.HIT_EFFECT:
            self.EFFECTS_CON.add_effect(self.HIT_EFFECT(*self._position, angle=self._angle))

    def make_creation_effect(self):
        if self.CREATION_EFFECT:
            self.EFFECTS_CON.add_effect(self.CREATION_EFFECT(*self._position, speed=self._speed,
                                                             head_len=self.size[0] + self.size[0] + self.size[0],
                                                             tail_len=self.size[0], width_len=self.size[0]/2,
                                                             fill=1,
                                                             angle=self.angle, arena=self.arena),
                                        layer=0)

    def additional_lazy_load(self):
        from visual.diamond_effect import DiamondEffect
        SimpleBullet.CREATION_EFFECT = DiamondEffect
        # SimpleBullet

    def update(self):
        self._update()

    def _draw(self):
        dx, dy = GLOBAL_CAMERA.camera
        x, y = self.int_position

        picture = self.ROTATE(self._picture, -degrees(self._angle))
        self.MAIN_SCREEN.blit(picture, (x - picture.get_width() // 2 + dx, y - picture.get_height() // 2 + dy))

    def interact_with_object(self, object):
        self.make_hit_effect()
        object.damage(self.damage)
        if self._push_force != 0.0:
            pos = self.owner.position if self.owner else self.position
            object.push(pos, self._push_force)

        self.kill()

    def kill(self):
        self.make_death_effect()
        self._alive = 0
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
            'NAME': self.NAME,
            'TYPE': self.TYPE,
        }

    @staticmethod
    def alive_condition(self):
        return self._speed > 0
