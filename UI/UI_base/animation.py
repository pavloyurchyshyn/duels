from settings.window_settings import MAIN_SCREEN
from pygame import transform
from math import degrees


class Animation:
    MAIN_SCREEN = MAIN_SCREEN

    def __init__(self, position: [int, int], idle_frames: list, current_anim='idle', angle=0, **kwargs):
        """
        :param position: position of animation
        :type position: int, int
        :param idle_frames: should be like {0: {'frame': picture, 'cd': float} or with 'end'}
        :type idle_frames: list
        :param angle: radians
        :param kwargs:
        """
        self.x, self.y = position

        self._angle = -degrees(angle)
        self.current_anim = current_anim
        self.frame = 0

        self.animations = {
            'idle': idle_frames
        }

        self._time = 0
        self._t_delay = 0

        self.animations.update(**kwargs)

        self.image = self.animations['idle'][self.frame]['frame']

        self.next_frame = self._time + self.animations[self.current_anim][self.frame]['cd']

    def update(self, d_time, position=None, angle=None):
        self._t_delay = d_time
        self._time += d_time

        if angle is not None:
            self._angle = -degrees(angle)

        if position is not None:
            self.x, self.y = position

        if self._time >= self.next_frame:
            self.frame += 1
            if self.frame not in self.animations[self.current_anim]:
                self.frame = 0
                if 'end' in self.animations[self.current_anim]:
                    self.current_anim = self.animations[self.current_anim]['end']

            self.image = self.animations[self.current_anim][self.frame]['frame']

            self.next_frame = self._time + self.animations[self.current_anim][self.frame]['cd']

    def draw(self, dx, dy):
        img_copy = transform.rotate(self.image, self._angle)

        Animation.MAIN_SCREEN.blit(img_copy,
                                   (self.x - img_copy.get_width() // 2 + dx,
                                    self.y - img_copy.get_height() // 2 + dy))

    def change_animation(self, animation):
        if animation == self.current_anim:
            return

        if animation not in self.animations:
            raise Exception(f'Bad animation key {animation}')

        self.current_anim = animation
        self.frame = 0
        self.next_frame = self._time + self.animations[self.current_anim][self.frame]['cd']

    def set_anim(self, value):
        if value in self.animations:
            self.current_anim = value
            self.next_frame = self._time + self.animations[self.current_anim][self.frame]['cd']
            self.image = self.animations[self.current_anim][self.frame]['frame']

    @property
    def position(self):
        return self.x, self.y

    @position.setter
    def position(self, value):
        self.x, self.y = value


class RotateAnimation:
    MAIN_SCREEN = MAIN_SCREEN

    def __init__(self, position, image, rotating_speed=30, angle=0):
        """
        :param position: center position
        :param image: image
        :param rotating_speed: degrees 
        """
        self.image = image
        self.x, self.y = position
        self.rotating_speed = rotating_speed
        self._angle = angle

    def update(self, d_time, position=None, angle=None):
        if angle is not None:
            self._angle = angle

        if position is not None:
            self.x, self.y = position

        if self.rotating_speed:
            self._angle += self.rotating_speed * d_time

    def draw(self, dx, dy):
        img_copy = transform.rotate(self.image, self._angle)

        Animation.MAIN_SCREEN.blit(img_copy,
                                   (self.x - img_copy.get_width() // 2 + dx,
                                    self.y - img_copy.get_height() // 2 + dy))