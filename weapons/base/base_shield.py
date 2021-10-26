from obj_properties.circle_form import Circle
from obj_properties.lazy_load_mixin import PictureLazyLoadMixin
from math import degrees
from common_things.camera import GLOBAL_CAMERA

from common_things.common_objects_lists_dicts import BULLETS_LIST
from common_things.global_clock import GLOBAL_CLOCK


class DefaultShield(Circle, PictureLazyLoadMixin):
    def __init__(self, x, y, R: int, cooldown=-1, mortal=True, health_points=100, all_time_active=False):
        super().__init__(x=x, y=y, R=R)

        self.mortal = mortal
        self._full_health_points = health_points
        self._health_points = health_points
        self._all_time_active = all_time_active
        self._use = False
        self.use_cooldown = cooldown
        self.cooldown = -1
        self.dt = GLOBAL_CLOCK.d_time

        PictureLazyLoadMixin.__init__(self)

    def update(self):
        self.dt = GLOBAL_CLOCK.d_time
        if self.cooldown > 0:
            self.cooldown -= self.dt

        if self._all_time_active:
            self._check_for_bullets()

        elif self._use:
            self._use = 0
            self._check_for_bullets()

    def use(self):
        if self.cooldown < 0:
            self.cooldown = self.use_cooldown
            self._use = 1

    def _check_for_bullets(self):
        for bullet in BULLETS_LIST:
            if bullet.alive and self.collide_circle(bullet.position, bullet.size):
                bullet.kill()
                if self.mortal:
                    self.damage(bullet.damage)
                    if self._health_points < 0:
                        break

    def __lazy_load(self):
        self._lazy_load_picture()
        self.draw = self.__draw
        self.draw()

    def __draw(self):
        dx, dy = GLOBAL_CAMERA.camera
        x, y = self.int_position

        picture = self._picture_rotate(self._picture, -degrees(self._angle))
        self._main_screen.blit(picture, (x - picture.get_width() // 2 + dx, y - picture.get_height() // 2 + dy))

    def damage(self, damage):
        self._health_points -= damage

    @property
    def alive(self):
        return not self.mortal or self._health_points > 0
