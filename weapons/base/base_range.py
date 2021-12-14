from common_things.global_clock import GLOBAL_CLOCK
from common_things.camera import GLOBAL_CAMERA

from obj_properties.circle_form import Circle
from obj_properties.lazy_load_mixin import PictureLazyLoadMixin
from obj_properties.objects_data_creator import objects_data_creator

from settings.weapon_settings.base_range import *
from settings.global_parameters import test_draw_status_is_on

from weapons.base.base_bullet import SimpleBullet
from math import degrees


class BaseRange(Circle, PictureLazyLoadMixin):
    DEFAULT_COOLDOWN = DEFAULT_COOLDOWN
    PICTURE_PATH = DEFAULT_PICTURE_PLACE
    DEFAULT_SIZE = DEFAULT_SIZE
    SHOOT_EFFECT = None

    def __init__(self, x, y, arena, owner=None, size=None, bullet: str=SimpleBullet.NAME):
        size = size if size else BaseRange.DEFAULT_SIZE

        self._picture = BaseRange.PICTURE
        self._main_screen = BaseRange.MAIN_SCREEN
        self._picture_rotate = BaseRange.ROTATE  # pygame transform.rotate

        super().__init__(x=x, y=y, R=size, dots_angle=1)
        PictureLazyLoadMixin.__init__(self)

        self.dt = 0
        self.owner = owner
        self.shoot_cooldown = self.DEFAULT_COOLDOWN
        self.cooldown = 1
        self._use = 0

        self._angle = 0
        self._bullet_type: str = bullet
        self._arena = arena

    def update(self, angle, position):
        self.dt = GLOBAL_CLOCK.d_time
        if self.cooldown < 0:
            self.cooldown += self.dt

        self._angle = angle
        self._change_position(position, make_dots=1)

    def shoot(self):
        if self.SHOOT_EFFECT:
            self.SHOOT_EFFECT(*self._center, angle=self._angle, arena=self._arena)

        self._arena.add_object(objects_data_creator(name=self._bullet_type,
                                                    data={
                                                        'x': self._center[0],
                                                        'y': self._center[1],
                                                        'angle': self._angle,
                                                    }))

    def use(self):
        if self.cooldown > 0:
            self.cooldown = -self.shoot_cooldown
            self.shoot()

    def alt_use(self):
        pass

    def _draw(self):
        dx, dy = GLOBAL_CAMERA.camera
        m_screen = self.MAIN_SCREEN
        x0, y0 = self._center

        picture = self.ROTATE(self._picture, -degrees(self._angle))
        m_screen.blit(picture, (x0 + dx - picture.get_width() // 2, y0 + dy - picture.get_height() // 2))

        self.DRAW_CIRCLE(m_screen, (255, 0, 0), (x0 + dx, y0 + dy), 5)
        self.DRAW_CIRCLE(m_screen, (255, 255, 0), (self._dots[1][0] + dx, self._dots[1][1] + dy), 1)

        if test_draw_status_is_on:
            for (x, y) in self._dots:
                self.DRAW_CIRCLE(m_screen, (0, 0, 255), (x + dx, y + dy), 1)

    def additional_lazy_load(self):
        from visual.shoot_effect import ShootEffect

        BaseRange.SHOOT_EFFECT = ShootEffect

    @property
    def size(self):
        return self.DEFAULT_SIZE, self.DEFAULT_SIZE