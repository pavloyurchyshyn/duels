from obj_properties.base_projectile import Projectile
from obj_properties.img_lazy_load import OnePictureLazyLoad, AdditionalLazyLoad
from obj_properties.point import Point

from settings.weapon_settings.base_bullet import *
from settings.weapon_settings.types_and_names import BULLETS_TYPE, SIMPLE_BULLET
from settings.game_objects_constants import ANGLE_CHANGE_P_SEC, STOP_FORCE_K, STOP_FORCE_VALUE

from math import degrees

from common_things.all_objects_names_classes_dict import all_names_objects_dict_wrapper
from common_things.camera import GLOBAL_CAMERA
from common_things.common_objects_lists_dicts import PLAYERS_DICT, OBJECTS_LIST
from common_things.loggers import LOGGER


@all_names_objects_dict_wrapper
class SimpleBullet(Projectile, OnePictureLazyLoad, Point, AdditionalLazyLoad):
    OBJ_TYPE = BULLETS_TYPE
    OBJ_NAME = SIMPLE_BULLET

    PICTURE_PATH = DEFAULT_BULLET_PICTURE

    CREATION_EFFECT = None
    DEATH_EFFECT = None
    HIT_EFFECT = None

    def __init__(self, x, y,
                 angle: float,
                 owner,
                 speed: float = None,
                 size: float = None,
                 damage=None,
                 push_force=300,
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
        OnePictureLazyLoad.__init__(self)
        AdditionalLazyLoad.__init__(self)

        self._picture = SimpleBullet.PICTURE
        self._main_screen = SimpleBullet.MAIN_SCREEN
        self._picture_rotate = SimpleBullet.ROTATE  # pygame transform.rotate
        self.owner = owner

        self.damage = damage if damage else DEFAULT_BULLET_DAMAGE
        self._push_force = push_force

        self.make_creation_effect()

    def make_death_effect(self):
        if self.DEATH_EFFECT:
            self.DEATH_EFFECT(*self.position, angle=self._angle)

    def make_hit_effect(self):
        if self.HIT_EFFECT:
            self.EFFECTS_CON.add_effect(self.HIT_EFFECT(*self._position, angle=self._angle))

    def make_creation_effect(self):
        if self.CREATION_EFFECT:
            self.CREATION_EFFECT(*self._center)

    def additional_lazy_load(self):
        from visual.simple_bullet_effects import bullet_death_effect
        SimpleBullet.DEATH_EFFECT = bullet_death_effect

        # from visual.diamond_effect import DiamondEffect
        # SimpleBullet.CREATION_EFFECT = DiamondEffect
        # SimpleBullet

    def update(self):
        self._update()
        self.check_for_players_intersection()
        self.check_for_object_intersection()

    def check_for_object_intersection(self):
        for obj in OBJECTS_LIST:
            if obj != self.owner and obj.collide(self):
                self.interact_with_object(obj)

    def check_for_players_intersection(self):
        for player in PLAYERS_DICT.values():
            if player != self.owner and player.collide(self):
                self.interact_with_object(player)
                player._visual_part.hit_effect(*self.position, self._angle, arena=self.arena)

    def draw(self):
        dx, dy = GLOBAL_CAMERA.camera
        x, y = self.int_position

        picture = self.ROTATE(self._picture, -degrees(self._angle))
        self.MAIN_SCREEN.blit(picture, (x - picture.get_width() // 2 + dx, y - picture.get_height() // 2 + dy))

    def interact_with_object(self, object):
        self.make_hit_effect()
        object.damage(self.damage)
        LOGGER.info(f'Bullet {self.__dict__} damaged {object.__dict__}')
        if self._push_force != 0.0:
            # pos = self.owner.position if self.owner else self.position
            object.push(force=self._push_force, angle=self._angle)

        self.kill()

    def kill(self):
        self.make_death_effect()
        self._alive = 0
        self.stop()

    @property
    def __dict__(self):
        return {
            'NAME': self.OBJ_NAME,
            'TYPE': self.OBJ_TYPE,
            'GLOBAL_KEY': self.GLOBAL_KEY,
            'x': self._position[0],
            'y': self._position[1],
            'size': self.size[0],
            'angle': self._angle,
            'speed': self._speed,
            ANGLE_CHANGE_P_SEC: self._angle_change,
            STOP_FORCE_K: self._stop_force_k,
            STOP_FORCE_VALUE: self._stop_force_value,

        }

    @staticmethod
    def alive_condition(self):
        return self._speed > 0
