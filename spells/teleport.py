from common_things.global_clock import ROUND_CLOCK
from common_things.global_mouse import GLOBAL_MOUSE
from common_things.camera import GLOBAL_CAMERA
from math import cos, sin, dist
from visual.teleport_effect import TeleportEffect
from visual.visual_effects_controller import VisualEffectsController
from settings.global_parameters import its_client_instance


class Teleport:
    CD = 1

    def __init__(self, player, arena=None, **kwargs):
        self._player = player
        self._next_teleport = 1
        self._clock = ROUND_CLOCK
        self._arena = arena if arena else player._arena
        self._camera = self._player.camera
        self._tp_range = 500
        self._visual_effect = TeleportEffect

    def update(self):
        if self._next_teleport < 0:
            self._next_teleport += self._clock.d_time

    def use(self, camera=its_client_instance):
        if self._next_teleport > 0:
            angle = self._player.angle
            x_mouse, y_mouse = GLOBAL_MOUSE.pos
            x_player, y_player = self._player.position

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
                    if dist(last_dot, self._player.position) >= m_dist:
                        break
                else:
                    break

            if last_dot:
                self._next_teleport = -self.CD
                VisualEffectsController.add_effect(self._visual_effect(self._player.position, last_dot,
                                                                       radius=self._player.get_size() * 2))
                self._player.position = last_dot
