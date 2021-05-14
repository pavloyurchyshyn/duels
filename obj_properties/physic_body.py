from obj_properties.vector2d import Vector_2d

from common_things.global_clock import GLOBAL_CLOCK

from world_arena.world import GLOBAL_WORLD

from math import sin, cos, pi, atan2, sqrt, radians, dist
from abc import abstractmethod, ABC


class PhysicalObj:
    clock = GLOBAL_CLOCK
    world = GLOBAL_WORLD

    def __init__(self, mass: float, f_coef: float = 0.70):
        self._f_coef = f_coef
        self._mass = mass  # mass
        self._velocity = Vector_2d(0, 0)

    def _push_another_items(self) -> None:
        items = self.item_con.items
        try:
            idx = items.index(self)
        except ValueError:
            idx = 0

        for item in items[idx:]:
            # item = items[i]
            if item is self:
                continue

            if self.collide_dots(item):
                if self._velocity:
                    if dist((self._center[0] + self._velocity.vector[0], self._center[1] + self._velocity.vector[1]),
                            item._center) < dist(self._center, item._center):
                        vector = self._velocity.vector
                        vector = vector[0] * 1.2, vector[1] * 1.2
                        item.push(vector=vector)
                        self._velocity.reverse()
                        self._velocity.mul_k(0.1)
                else:
                    item.push(self._center, self._mass / self._d_time)

    def _push_units(self) -> None:
        for units in self.un_con.units:
            for unit in units:
                if unit is self:
                    continue

                if unit.collide(self):
                    unit.push(self._mass * (self._a if self._a > 0 else 1))
                    self._a = -1
                    return

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

            self._velocity.x += vec_x * self._d_time
            self._velocity.y += vec_y * self._d_time

        if vector is not None:
            self._velocity.x += vector[0]
            self._velocity.y += vector[1]

        if pos == angle == vector is None:
            raise Exception('Bad arguments')

    @abstractmethod
    def use_self_force(self) -> None:
        if bool(self._velocity):
            self._use_self_force()
            self._push_another_items()

    def _use_self_force(self) -> None:
        if bool(self._velocity):
            # print(1 - (1 - self._f_coef) * self._d_time, self._d_time)
            self._velocity.mul_k(self._f_coef)

            x, y = self._center

            new_x = x + self._velocity.x  # * self._d_time
            new_y = y + self._velocity.y  # * self._d_time

            if self._arena.can_go(new_x, new_y):
                pass
                self._change_position((new_x, new_y))
                self._make_dots()
            else:
                self._velocity.zero()

    def push_me(self, obj, force=None):
        try:
            force = force if force is not None else self._mass * self._a
        except ZeroDivisionError:
            force = 1

        obj.push(self._center, force)


    def stop(self):
        self._velocity.stop()
