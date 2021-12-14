from math import sin, cos, radians, degrees
from interfaces.collide_interfaces import CollideInterface
from settings.game_objects_constants import *
from common_things.global_clock import ROUND_CLOCK, GLOBAL_CLOCK
from abc import abstractmethod
from interfaces.any_object_interface import AnyObjInterface
from visual.visual_effects_controller import VisualEffectsController


class Projectile(AnyObjInterface):
    def __init__(self, x: int, y: int,
                 speed: float, angle: float,
                 arena,
                 round_clock=1,
                 collide_shape: CollideInterface = None,
                 x_step_func=None, y_step_func=None,
                 on_death_effect=None,
                 stop_if_out_of_arena=1,
                 **kwargs):
        super().__init__()

        self.arena = arena
        self._position = [x, y]
        self._angle = angle

        self._stop_if_out_of_arena = stop_if_out_of_arena

        self._angle_k = [cos(angle), sin(angle)]
        self.calculate_angle_k()

        self._angle_change: float = kwargs.get(ANGLE_CHANGE_P_SEC)
        self._speed: float = speed
        self._stop_force_value: float = kwargs.get(STOP_FORCE_VALUE)
        self._stop_force_k: float = kwargs.get(STOP_FORCE_K)

        self.collide_shape: CollideInterface = collide_shape
        self._x_step_func = x_step_func if x_step_func else self.__simple_x_step
        self._y_step_func = y_step_func if y_step_func else self.__simple_y_step
        self.on_death_effect = on_death_effect

        self._alive = 1
        self._clock = ROUND_CLOCK if round_clock else GLOBAL_CLOCK
        self._d_time = 0

    @abstractmethod
    def update(self):
        self._update()

    def _update(self, delta_time: float = None):
        if self._alive:
            if not delta_time:
                self._d_time = delta_time = self._clock.d_time

            self.change_angle(delta_time)

            self.make_step()

            self.use_stop_force()

            if self._stop_if_out_of_arena and self.out_of_arena():
                self.stop()

        self._alive = self.alive_condition(self)

    # @abstractmethod
    # def alive_condition(self):
    #     raise NotImplementedError

    def out_of_arena(self):
        return not self.arena.collide_point(self._position)

    def in_arena(self):
        return self.arena.collide_point(self._position)

    def change_angle(self, delta_time=1):
        if self._angle_change:
            self._angle += self._angle_change * delta_time
            self.calculate_angle_k()

    @staticmethod
    def __simple_x_step(self):
        if self._speed:
            self._position[0] += self._angle_k[0] * self._speed * self._clock.d_time

    @staticmethod
    def __simple_y_step(self):
        if self._speed:
            self._position[1] += self._angle_k[1] * self._speed * self._clock.d_time

    def make_step(self):
        self._x_step_func(self)
        self._y_step_func(self)

        if self.collide_shape:
            self.collide_shape._change_position(self._position)

    def use_stop_force(self):
        if self._stop_force_value:
            delta_time = self._clock.d_time

            if self._speed > 0.0:
                self._speed -= self._stop_force_value * delta_time
                if self._speed < 0.0:
                    self.stop()

            else:
                self._speed += self._stop_force_value * delta_time
                if self._speed > 0.0:
                    self.stop()

        # if self._stop_force_k is not None:
        #     self._speed *= self._stop_force_k * delta_time
        if -0.01 < self._speed < 0.01:
            self.stop()

    def start_dead_effect(self):
        if self.on_death_effect:
            VisualEffectsController.add_effect(self.on_death_effect(*self._position, angle=self._angle))

    def calculate_angle_k(self):
        self._angle_k = [cos(self._angle), sin(self._angle)]

    def stop(self):
        self._speed = 0.0

    def reverse_moving(self):
        self._speed = -self._speed

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        self._position = new_position

    @property
    def int_position(self):
        return int(self._position[0]), int(self._position[1])

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, new_angle):
        self._angle = new_angle
        self.calculate_angle_k()

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, new_speed):
        self._speed = new_speed

    def collide(self, shape_object) -> bool:
        if self.collide_shape is not None:
            return self.collide_shape.collide(shape_object)
        else:
            return False

    def collide_point(self, xy) -> bool:
        if self.collide_shape is not None:
            return self.collide_shape.collide_point(xy)
        else:
            return False

    def collide_dots(self, xy) -> bool:
        if self.collide_shape is not None:
            return self.collide_shape.collide_dots(xy)
        else:
            return False

    @property
    def alive(self):
        return self._alive

    @property
    def dead(self):
        return not self._alive
