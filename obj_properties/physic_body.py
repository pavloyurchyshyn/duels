from obj_properties.vector2d import Vector_2d

from common_things.global_clock import GLOBAL_CLOCK

from math import sin, cos, pi, atan2, sqrt, radians, dist
from abc import abstractmethod, ABC


class PhysicalObj:
    def __init__(self, mass: float=1, f_coef: float = 2):
        self._f_coef = f_coef
        self._mass = mass

        self._velocity = Vector_2d(0, 0)

    @abstractmethod
    def push(self, pos=None, force=None, angle=None, vector=None):
        self._push(pos=pos, force=force, angle=angle, vector=vector)

    def _push(self, pos: tuple = None, force: int = 0, angle: float = None, vector: tuple = None) -> None:
        if force and (pos is not None or angle is not None):
            if pos:
                x1, y1 = self._center
                x, y = pos
                d_x = 0.00001 if x1 - x == 0 else x1 - x
                d_y = 0.00001 if y1 - y == 0 else y1 - y

                angle = atan2(d_y, d_x)

            elif angle is not None:
                pass

            else:
                raise Exception('No pos and No angle')

            vec_x = cos(angle) * force
            vec_y = sin(angle) * force

            self._velocity.x += vec_x
            self._velocity.y += vec_y

        if vector is not None:
            self._velocity.x += vector[0]
            self._velocity.y += vector[1]

        if pos == angle == vector is None:
            raise Exception('Bad arguments')

    @abstractmethod
    def use_self_force(self, inside_borders=0) -> None:
        self._use_self_force(inside_borders)

    def _use_self_force(self, inside_borders=0) -> None:
        if self._velocity:
            self._velocity.mul_k(1 - self._f_coef*self._d_time)
            x, y = self._center

            new_x = x + self._velocity.x * self._d_time
            new_y = y + self._velocity.y * self._d_time
            can_move = not self._arena.check_for_exit((new_x, new_y)) if inside_borders else self._arena.collide_point((new_x, new_y))
            if can_move:
                self._change_position((new_x, new_y))
                self._make_dots()
            else:
                self._velocity.stop()
    def reverse(self):
        self._velocity.reverse()

    def stop(self):
        self._velocity.stop()
