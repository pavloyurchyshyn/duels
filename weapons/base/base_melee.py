from common_things.camera import GLOBAL_CAMERA
from common_things.all_objects_names_classes_dict import all_names_objects_dict_wrapper
from common_things.common_objects_lists_dicts import PLAYERS_DICT, OBJECTS_LIST

from obj_properties.img_lazy_load import OnePictureLazyLoad, AdditionalLazyLoad
from obj_properties.line import Line

from object_controller import AllObjectsController

from player.player_effects import OWNER_EFFECT, TARGET_EFFECT
from player.base.base_player import BasePlayer

from settings.weapon_settings.types_and_names import MELEE_HIT_TYPE, SIMPLE_MELEE_HIT
from settings.weapon_settings.base_melee import *
from settings.global_parameters import test_draw_status_is_on

from weapons.base.base_weapon import BaseWeapon

from math import degrees, cos, sin, radians


class BaseMelee(BaseWeapon, OnePictureLazyLoad):
    PICTURE_PATH = 'sabre.png'
    CD = -1
    _all_obj_controller = AllObjectsController()

    def __init__(self, x, y, owner, size_x=DEFAULT_SIZE, size_y=None, melee_hit_obj=None, **kwargs):
        BaseWeapon.__init__(self)
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y if size_y else size_x
        self.size = (10, 70)

        self._owner: BasePlayer = owner
        self._camera = getattr(self._owner, 'camera', GLOBAL_CAMERA)

        OnePictureLazyLoad.__init__(self, size=self.size)

        self._owner_effects = kwargs.get(OWNER_EFFECT, {})
        self._target_effects = kwargs.get(TARGET_EFFECT, {})
        self._melee_hit_obj = melee_hit_obj if melee_hit_obj else BaseMeleeHit.OBJ_NAME

        self._angle = self._owner.angle
        self._anim_time = 0.25

        self._add_draw_angle = 0.
        self._min_add_angle = radians(-90)
        self._max_add_angle = radians(90)
        self._angle_step_per_sec = radians(180) / self._anim_time

        self.cooldown = 1

    def additional_lazy_load(self):
        pass

    def use(self):
        if self.cooldown >= 0.0:
            self._add_draw_angle = self._min_add_angle

            self.cooldown = self.CD
            # MELEE_HITS_LIST.append(self._melee_hit_obj(self.x, self.y, angle=self._angle,
            #                                            owner=self.owner, damage=50, length=50))
            self._all_obj_controller.add_object({'name': self._melee_hit_obj,
                                                 'data': {'x': self.x, 'y': self.y, 'angle': self._angle,
                                                          'owner': self._owner._unique_id}})

    def alt_use(self):
        pass

    def update(self, angle, position):
        self._update(angle, position)

    def _update(self, angle, position):
        self._angle = angle
        d_time = self._owner._d_time

        if self._add_draw_angle != 0.:
            self._add_draw_angle += self._angle_step_per_sec * d_time
            if self._add_draw_angle > self._max_add_angle:
                self._add_draw_angle = 0.

        self.x, self.y = position
        if self.cooldown < 0.0:
            self.cooldown += d_time

    def draw(self):
        dx, dy = self._camera.camera
        is_active_weapon = self == getattr(self._owner, '_active_weapon', 0)
        add_a = 0 if is_active_weapon else 90
        img_copy = self.ROTATE(self.PICTURE, -degrees(self._angle + self._add_draw_angle) + add_a)

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


@all_names_objects_dict_wrapper
class BaseMeleeHit(Line, AbstractMeleeHit, AdditionalLazyLoad):
    OBJ_TYPE = MELEE_HIT_TYPE
    OBJ_NAME = SIMPLE_MELEE_HIT

    CREATION_EFFECT = None
    HIT_EFFECT = None

    def __init__(self, x, y, angle, owner, length=50, damage=50, *args, **kwargs):
        super(BaseMeleeHit, self).__init__(xy0=(x, y), angle=angle, length=length)
        self._alive = 1
        self._owner = owner
        self._damage = damage
        self._alive_time = 0.6
        self._d_time = self._owner._d_time
        self.creation_effect()
        AdditionalLazyLoad.__init__(self)
        self.damaged_objects = set()

    def additional_lazy_load(self):
        if not BaseMeleeHit.HIT_EFFECT:
            from visual.simple_hit_effect import base_hit_effect_func

            BaseMeleeHit.HIT_EFFECT = base_hit_effect_func

    def hit_visual_effect(self):
        if self.HIT_EFFECT:
            self.HIT_EFFECT(x=self.x1, y=self.y1, angle=self._angle)

    def creation_effect(self):
        if self.CREATION_EFFECT:
            pass

    def update(self):
        self._alive_time -= self._owner._d_time
        self._d_time = self._owner._d_time
        self._alive = self._alive_time > 0
        self.check_for_object_intersection()
        self.check_for_players_intersection()

    def check_for_object_intersection(self):
        for obj in OBJECTS_LIST:
            if obj.collide(self):
                self.interact_with_object(obj)

    def check_for_players_intersection(self):
        for player in PLAYERS_DICT.values():
            if player != self._owner and player.collide(self):
                self.interact_with_object(player)

    def interact_with_object(self, object):
        if object not in self.damaged_objects:
            object.damage(self._damage)
            object.push(force=1000, angle=self._angle)
            self.hit_visual_effect()
            self.damaged_objects.add(object)

    @property
    def alive(self):
        return self._alive
