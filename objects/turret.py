from obj_properties.circle_form import Circle
from common_things.global_clock import GLOBAL_CLOCK
from common_things.camera import GLOBAL_CAMERA
from common_things.common_objects_lists_dicts import PLAYERS_DICT
from common_things.common_functions import get_angle_between_dots
from math import dist, cos, sin
from settings.objects_settings.turret_settings import *
from object_controller import AllObjectsController
from weapons.base.base_bullet import SimpleBullet


class Turret(Circle):
    obj_controller = AllObjectsController()
    _camera = GLOBAL_CAMERA

    def __init__(self, x, y):
        super().__init__(x=x, y=y, R=R_SIZE)
        self._barrel_len = 30
        self._reload_time = -RELOAD_TIME
        self._reloading = 0.

        self._max_bullets_in_mag = BULLETS_IN_MAG
        self._bullets_in_mag = BULLETS_IN_MAG

        self._time_per_shoot = -PER_SHOOT_TIME
        self._next_shoot = 0

        self._clock = GLOBAL_CLOCK

        self._angle = 0.
        self._max_dist_to_player = 500

        self._players_dict = PLAYERS_DICT

        self._current_target = None

        self._bullet_type = SimpleBullet.OBJ_NAME

    def update(self):
        d_time = self._clock.d_time
        if self._bullets_in_mag == 0:
            if self._reloading < 0:
                self._reloading += d_time
            else:
                self._bullets_in_mag = self._max_bullets_in_mag
                self._next_shoot = 1
        else:
            self.find_closest_target()

            if self._current_target:
                self._angle = get_angle_between_dots(self._center, self._current_target.position)
                if self._next_shoot > 0:
                    self.obj_controller.add_object(dict(name=self._bullet_type,
                                                        data={
                                                            'x': self._center[0],
                                                            'y': self._center[1],
                                                            'angle': self._angle,
                                                            'owner': self,
                                                        }))

                    self._bullets_in_mag -= 1
                    self._next_shoot = self._time_per_shoot

                    if self._bullets_in_mag < 1:
                        self._bullets_in_mag = 0
                        self._reloading = self._reload_time
                        self._current_target = None
                else:
                    self._next_shoot += d_time

    def find_closest_target(self):
        self._current_target = None
        dist_to_target = 99999
        for player in self._players_dict.values():
            d = dist(player.position, self._center)
            if d <= self._max_dist_to_player and d < dist_to_target:
                self._current_target = player
                dist_to_target = d

    def draw(self):
        dx, dy = GLOBAL_CAMERA.camera
        x, y = self._center

        from pygame.draw import circle
        from pygame.draw import line
        from settings.window_settings import MAIN_SCREEN
        circle(MAIN_SCREEN, (0, 0, 0), (x + dx, y + dy), self._size)

        bx, by = (x + cos(self._angle) * self._barrel_len, y + sin(self._angle) * self._barrel_len)
        line(MAIN_SCREEN, (70, 70, 70), (x + dx, y + dy), (bx + dx, by + dy), 3)
        if self._current_target:
            tx, ty = self._current_target.position
            line(MAIN_SCREEN, (0, 255, 0), (x + dx, y + dy), (tx + dx, ty + dy)),

    def damage(self, dmg):
        pass

    def push(self, *args, **kwargs):
        pass

    @property
    def dead(self):
        return 0

    @property
    def alive(self):
        return 1
