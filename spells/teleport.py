from common_things.global_clock import ROUND_CLOCK
from common_things.global_mouse import GLOBAL_MOUSE
from common_things.camera import GLOBAL_CAMERA
from math import cos, sin, dist
from visual.base.visual_effects_controller import VisualEffectsController
from settings.global_parameters import its_client_instance
from spells.base_spell import SpellIcon
from obj_properties.img_lazy_load import AdditionalLazyLoad


class Teleport(SpellIcon, AdditionalLazyLoad):
    CD = 1

    def __init__(self, owner, arena=None, **kwargs):
        super().__init__()
        self._owner = owner
        self._next_teleport = 1
        self._clock = ROUND_CLOCK
        self._arena = arena if arena else owner._arena
        self._camera = getattr(self._owner, 'camera', GLOBAL_CAMERA)
        self._tp_range = 500
        self._visual_effect = None
        AdditionalLazyLoad.__init__(self, its_client_instance())

    def additional_lazy_load(self):
        from visual.teleport_effect import TeleportEffect

        self._visual_effect = TeleportEffect

    def update(self):
        if self._next_teleport < 0:
            self._next_teleport += self._clock.d_time

    def use(self, camera=its_client_instance):
        if self._next_teleport > 0:
            angle = self._owner.angle
            x_mouse, y_mouse = GLOBAL_MOUSE.pos
            x_player, y_player = self._owner.position

            if camera and 0:
                xm, ym = self._camera.camera
                x_player += xm
                y_mouse += ym

            m_dist = dist((x_mouse, y_mouse), (x_player, y_player))
            tp_range = self._tp_range if m_dist > self._tp_range else m_dist
            last_dot = None
            for r in range(0, int(tp_range) + 1, 10):
                x = x_player + cos(angle) * r
                y = y_player + sin(angle) * r

                if self._arena.collide_point((x, y)):
                    last_dot = x, y
                    if dist(last_dot, self._owner.position) >= m_dist:
                        break
                else:
                    break

            if last_dot:
                self._next_teleport = -self.CD
                VisualEffectsController.add_effect(self._visual_effect(self._owner.position, last_dot, round_clock=1,
                                                                       radius=self._owner.get_size() * 2,
                                                                       arena=self._arena))
                self._owner.position = last_dot

    @property
    def cooldown(self):
        return self._next_teleport

    @property
    def on_cooldown(self):
        return self._next_teleport < 0.0
