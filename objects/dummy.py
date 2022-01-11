from settings.objects_settings.dummy_settings import *
from settings.global_parameters import test_draw_status_is_on

from pygame import transform
from pygame.draw import circle
from math import degrees
from common_things.global_clock import ROUND_CLOCK

from obj_properties.img_lazy_load import OnePictureLazyLoad
from obj_properties.circle_form import Circle
from obj_properties.physic_body import PhysicalObj


class Dummy(Circle, PhysicalObj, OnePictureLazyLoad):
    PICTURE_PATH = 'player/player_jojo.png'

    def __init__(self, x, y,
                 arena, camera,
                 size=DUMMY_SIZE,
                 **kwargs):
        super().__init__(x, y, R=size)
        self.image_size = (size + size, size + size)
        PhysicalObj.__init__(self, f_coef=FRICTION_K)
        OnePictureLazyLoad.__init__(self, size=self.image_size, angle=-90)

        self._arena = arena
        self.camera = camera
        self._d_time = 0
        self._time = 0

        self.image = self.PICTURE

    def damage(self, damage):
        pass

    def update(self, *args, **kwargs):
        time_d = ROUND_CLOCK.d_time
        self._d_time = time_d
        self._time += time_d
        self.use_self_force(1)

    def draw(self) -> None:
        if self.image:
            dx, dy = self.camera.camera

            x0, y0 = self._center

            main_screen = self.MAIN_SCREEN

            img_copy = transform.rotate(self.image, -degrees(self._angle))
            main_screen.blit(img_copy, (x0 - img_copy.get_width() // 2 + dx, y0 - img_copy.get_height() // 2 + dy))

            if test_draw_status_is_on():
                for dot in self._dots:
                    circle(main_screen, (255, 0, 0), (dot[0] + dx, dot[1] + dy), 3)

    @property
    def dead(self):
        return 0
        # circle(main_screen,
        #        self.color['body'],
        #        (self._hands_endpoint[0] + dx, self._hands_endpoint[1] + dy),
        #        5)
