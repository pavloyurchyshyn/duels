from obj_properties.circle_form import Circle

from spells.base_spell import BaseSpellProjectile, SpellIcon

from visual.base.visual_effects_controller import VisualEffectsController

from common_things.global_clock import ROUND_CLOCK
from common_things.all_objects_names_classes_dict import all_names_objects_dict_wrapper

from settings.spells_settings.spells_constants import SPELL_TYPE
from settings.global_parameters import test_draw_status_is_on

from object_controller import AllObjectsController

from obj_properties.img_lazy_load import AdditionalLazyLoad


class PushSpell(SpellIcon):
    CD = -1
    _obj_controller = AllObjectsController()

    def __init__(self, owner, clock=ROUND_CLOCK, **kwargs):
        super().__init__()
        self._clock = clock
        self._owner = owner
        self._next_use = 1
        self._d_time = self._clock.d_time

    def update(self):
        if self._next_use < 0:
            self._next_use += self._clock.d_time
            self._d_time = self._clock.d_time

    def use(self):
        if self._next_use > 0:
            x, y = self._owner._hands_endpoint
            self._obj_controller.add_object({'name': Push.OBJ_NAME,
                                             'data': {
                                                 'x': x, 'y': y,
                                                 'angle': self._owner.angle,
                                                 'owner': self._owner._unique_id
                                             }})
            # Push(*self._owner._hands_endpoint, self._owner.angle, clock=self._clock, owner=self._owner)
            self._next_use = PushSpell.CD

    @property
    def cooldown(self):
        return self._next_use

    @property
    def on_cooldown(self):
        return self._next_use < 0.0


@all_names_objects_dict_wrapper
class Push(Circle, BaseSpellProjectile, AdditionalLazyLoad):
    OBJ_TYPE = SPELL_TYPE
    OBJ_NAME = 'push_projectile_spell'

    ON_CREATION_EFFECT = None

    def __init__(self, x, y, angle, clock, owner, alive_time=0.25, **kwargs):
        super().__init__(x=x, y=y, R=50, dots_angle=1, angle=angle)
        BaseSpellProjectile.__init__(self)
        AdditionalLazyLoad.__init__(self)

        self._clock = clock
        self.owner = owner
        self._d_time = self._clock.d_time
        self._alive_time = alive_time

        if self.ON_CREATION_EFFECT:
            VisualEffectsController.add_effect(self.ON_CREATION_EFFECT(*self._center,
                                                                       owner=self.owner,
                                                                       alive_time=0.25,
                                                                       width=5,
                                                                       width_scale=-4,
                                                                       angle=angle, round_clock=1,
                                                                       speed=10,
                                                                       )
                                               )

    @classmethod
    def additional_lazy_load(cls):
        if not cls.ON_CREATION_EFFECT:
            from visual.semi_circle_wave import SemiCircleWave
            cls.ON_CREATION_EFFECT = SemiCircleWave

    def interact_with_player(self, player):
        player.push(force=25000 * self._d_time, angle=self._angle)

    def interact_with_object(self, obj):
        obj.push(force=25000 * self._d_time, angle=self._angle)

    def draw(self):
        pass

    def update(self):
        self._d_time = self._clock.d_time
        self._alive_time -= self._d_time
        self._alive = self._alive_time > 0.

        self.check_for_players_intersection()
        self.check_for_objects_intersection()

        if test_draw_status_is_on():
            from pygame.draw import circle
            dx, dy = self.owner.camera.camera
            m_screen = self.owner.MAIN_SCREEN
            for dot in self._dots:
                x, y = dot
                circle(m_screen, (255, 255, 0), (x + dx, y + dy), 3)

    @property
    def position(self):
        return self._center
