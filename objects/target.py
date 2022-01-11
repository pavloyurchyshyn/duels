from obj_properties.rect_form import Rectangle
from obj_properties.img_lazy_load import LoadPictureMethodLazyLoad, ScreenLazyLoad, PygameMethodsLazyLoad, AdditionalLazyLoad
from obj_properties.physic_body import PhysicalObj
from settings.objects_settings.target_settings import *
from common_things.global_clock import ROUND_CLOCK
from common_things.camera import GLOBAL_CAMERA
from settings.global_parameters import its_client_instance


class Target(Rectangle, ScreenLazyLoad, LoadPictureMethodLazyLoad, PygameMethodsLazyLoad, PhysicalObj, AdditionalLazyLoad):
    def __init__(self, x, y, angle=0.0, eternal=1, physical=0, arena=None):
        super(Target, self).__init__(x, y, *target_size)
        ScreenLazyLoad.__init__(self)
        LoadPictureMethodLazyLoad.__init__(self)
        PygameMethodsLazyLoad.__init__(self)
        PhysicalObj.__init__(self)
        AdditionalLazyLoad.__init__(self)
        if its_client_instance():
            self.additional_load()

        self._angle = angle
        self._clock = ROUND_CLOCK
        self._eternal = eternal
        self._closed_time = -1
        self._closed = 1
        self._alive = 1
        self._physical = physical
        self._arena = arena
        if self._physical and not self._arena:
            raise Exception('send arena')
        self._hp = 100

        self._animation = None

    def additional_load(self):
        anim = self.LOAD_ANIMATION()
        self._animation = self.ANIMATION(self._center)
    def update(self):
        if self._closed < 0:
            self._closed += self._clock.d_time
            self._collide_able = 0

        else:
            self._collide_able = 1

        if self._physical:
            self.use_self_force(1)

    def draw(self):

    def damage(self, damage):
        if not self._eternal:
            self._hp -= damage
            self._alive = self._hp > 0

        self._closed = self._closed_time

    @property
    def alive(self):
        return self._alive

    @property
    def dead(self):
        return not self._alive