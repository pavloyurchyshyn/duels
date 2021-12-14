from interfaces.simple_weapon_interface import SimpleWeaponInterface
from obj_properties.line import Line
from obj_properties.circle_form import Circle
from math import dist
from settings.player_effects import OWNER_EFFECT, TARGET_EFFECT
from settings.weapon_settings.base_melee import *
from visual.visual_effects_controller import VisualEffectsController
from obj_properties.lazy_load_mixin import PictureLazyLoadMixin
from common_things.global_clock import ROUND_CLOCK


class BasicMelee(SimpleWeaponInterface):
    def __init__(self, x, y, size_x=DEFAULT_SIZE, size_y=None,
                 hitbox_radius=DEFAULT_HITBOX_SIZE, hitbox_angles=360, **kwargs):
        super().__init__(x=x, y=y, size_x=size_x, size_y=size_y)

        # self._attack_hitbox = Circle(x, y, hitbox_radius) if hitbox_angles >= 360 else HalfCircle(x, y, R=hitbox_radius, hitbox_angle=hitbox_angles)
        # self._attack_hitbox = Circle(x, y, hitbox_radius)
        # self._hitbox_angles = hitbox_angles if hitbox_angles and 0 < hitbox_angles < 360 else None
        self._owner_effects = kwargs.get(OWNER_EFFECT, {})
        self._target_effects = kwargs.get(TARGET_EFFECT, {})
        self._owner = kwargs.get('owner')

    def attack(self):
        pass

    def update(self):

    def draw(self):

class BasicMeleeHit(Line):
    ATTACK_SPEED = 500
    RADIUS = DEFAULT_HITBOX_SIZE
    clock = ROUND_CLOCK

    EFFECTS_CON = VisualEffectsController

    CREATION_EFFECT = None
    HIT_EFFECT = None
    DEATH_EFFECT = None

    def __init__(self, x, y, angle, owner):
        super(BasicMeleeHit, self).__init__(xy0=(x, y), angle=angle, length=1.)
        self.damage = 10
        self._push_force = 5
        self.owner = owner
        self._alive = 1



    def make_death_effect(self):
        if self.DEATH_EFFECT:
            self.EFFECTS_CON.add_effect(self.DEATH_EFFECT(*self.position, angle=self._angle))

    def make_hit_effect(self):
        if self.HIT_EFFECT:
            self.EFFECTS_CON.add_effect(self.HIT_EFFECT(*self.position, angle=self._angle))

    def make_creation_effect(self):
        if self.CREATION_EFFECT:
            self.EFFECTS_CON.add_effect(self.CREATION_EFFECT(),
                                        layer=0)

    def interact_with_object(self, object):
        self.make_hit_effect()
        object.damage(self.damage)
        if self._push_force != 0.0:
            pos = self.owner.position if self.owner else self.position
            object.push(pos, self._push_force)

        self.kill()

    def kill(self):
        self._alive = 0

    @property
    def alive(self):
        return self._alive