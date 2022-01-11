from abc import ABC

from common_things.camera import GLOBAL_CAMERA
from common_things.common_objects_lists_dicts import MELEE_HITS_LIST
from obj_properties.img_lazy_load import OnePictureLazyLoad
from obj_properties.line import Line
from player.player_effects import OWNER_EFFECT, TARGET_EFFECT
from settings.weapon_settings.types_and_names import MELEE_HIT_TYPE

from settings.weapon_settings.base_melee import *
from settings.global_parameters import test_draw_status_is_on

from weapons.base.base_weapon import BaseWeapon
from math import degrees, cos, sin


class BaseMelee(BaseWeapon, OnePictureLazyLoad):
    PICTURE_PATH = 'sabre.png'
    CD = -1

    def __init__(self, x, y, owner, size_x=DEFAULT_SIZE, size_y=None, melee_hit_obj=None, **kwargs):
        BaseWeapon.__init__(self)
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y if size_y else size_x
        self.size = (10, 70)

        self.owner = owner
        self._camera = getattr(self.owner, 'camera', GLOBAL_CAMERA)
        self._angle = self.owner.angle

        OnePictureLazyLoad.__init__(self, size=self.size)

        self._owner_effects = kwargs.get(OWNER_EFFECT, {})
        self._target_effects = kwargs.get(TARGET_EFFECT, {})
        self._melee_hit_obj = melee_hit_obj if melee_hit_obj else BaseMeleeHit

        self.cooldown = 1

    def additional_lazy_load(self):
        pass

    def use(self):
        if self.cooldown >= 0.0:
            self.cooldown = self.CD
            MELEE_HITS_LIST.append(self._melee_hit_obj(self.x, self.y, angle=self._angle,
                                                       owner=self.owner, damage=50, length=50))

    def alt_use(self):
        pass

    def update(self, angle, position):
        self._update(angle, position)

    def _update(self, angle, position):
        self._angle = angle
        self.x, self.y = position
        if self.cooldown < 0.0:
            self.cooldown += self.owner._d_time

    def draw(self):
        dx, dy = self._camera.camera
        is_active_weapon = self == getattr(self.owner, '_active_weapon', 0)
        add_a = 0 if is_active_weapon else 90
        img_copy = self.ROTATE(self.PICTURE, -degrees(self._angle) + add_a)

        add_x, add_y = img_copy.get_width() // 2, img_copy.get_height() // 2

        self.MAIN_SCREEN.blit(img_copy, (self.x - add_x + dx, self.y - add_y + dy))
        if test_draw_status_is_on():
            x1 = self.x + cos(self._angle) * 50
            y1 = self.y + sin(self._angle) * 50
            self.DRAW_LINE(self.MAIN_SCREEN, (255, 255, 0), (self.x + dx, self.y + dy), (x1 + dx, y1 + dy))


class AbstractMeleeHit:
    def interact_with_object(self, object):
        raise NotImplementedError

    @property
    def alive(self):
        return self._alive

    @property
    def dead(self):
        return not self._alive


class BaseMeleeHit(Line, AbstractMeleeHit):
    TYPE = MELEE_HIT_TYPE
    CREATION_EFFECT = None

    def __init__(self, x, y, angle, length, owner, damage):
        super(BaseMeleeHit, self).__init__(xy0=(x, y), angle=angle, length=length)
        self._alive = 1
        self._owner = owner
        self._damage = damage
        self._alive_time = 0.6
        self._d_time = self._owner._d_time

    def creation_effect(self):
        if self.CREATION_EFFECT:
            pass

    def update(self):
        self._alive_time -= self._owner._d_time
        self._d_time = self._owner._d_time
        self._alive = self._alive_time > 0

    def interact_with_object(self, object):
        object.damage(self._damage)
        object.push(force=10000*self._d_time, angle=self._angle)

    @property
    def alive(self):
        return self._alive
