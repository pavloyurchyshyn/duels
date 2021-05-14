from settings.player_settings import *
from UI.message import Messages
from pygame.constants import *
from pygame import mouse, key, transform, Surface
from pygame.draw import circle, line, polygon
from visual_effects.animation import Animation

import time

from math import atan2, cos, sin, degrees, dist

from settings.common_settings import GLOBAL_SETTINGS, MAIN_SCREEN

import random


class SimplePlayer:
    MAIN_SCREEN = MAIN_SCREEN

    def __init__(self, x=0, y=0, scaled=False, dummy=True, **kwargs):
        self._angle = 0
        self.center = x, y

        self.image = PLAYER_PIC if not scaled else SCALED_PLAYER_PIC

        self._full_hp = PLAYER_HP
        self._hp = self._full_hp

        self.global_settings = GLOBAL_SETTINGS

        # =======================================
        self.cursor(mouse.get_pos())

        self.messages = Messages((x + 50, y))

        idle = IDLE_ANIMATION if not scaled else SCALED_IDLE_ANIMATION
        self.face_anim = Animation(self.center, idle_frames=idle, **OTHER_ANIMATIONS)

        self.dummy = dummy
        self._t_delay = 0
        self._time = 0

    def update(self, d_time, angle=None):
        self._time += d_time
        self._t_delay = d_time

        if angle is not None:
            self._angle = angle

        if not self.dummy:
            m_pos = mouse.get_pos()

            self.cursor(m_pos)

        self.messages.update(d_time, position=self.center)

        self.face_anim.update(d_time, self.center, self._angle)

    def cursor(self, m_pos: tuple):
        x1, y1 = m_pos
        xc, yc = self.center

        d_x = 0.00001 if x1 - xc == 0 else x1 - xc
        d_y = 0.00001 if y1 - yc == 0 else y1 - yc

        angle = atan2(d_y, d_x)

        self._angle = angle

    def draw(self) -> None:
        x0, y0 = self.center
        # circle(SimplePlayer.MAIN_SCREEN, (255, 255, 255), mouse.get_pos(), 3)  # draw mouse pos
        img_copy = transform.rotate(self.image, -degrees(self._angle))

        SimplePlayer.MAIN_SCREEN.blit(img_copy, (x0 - img_copy.get_width() // 2, y0 - img_copy.get_height() // 2))

        self.face_anim.draw(0, 0)

    @property
    def position(self):
        return self.center

    @position.setter
    def position(self, pos):
        self.center = pos
        # self.face_anim.position = pos

    @property
    def full_hp(self):
        return self._full_hp

    @full_hp.setter
    def full_hp(self, hp):
        self._full_hp = hp

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value

    def set_anim(self, anim):
        self.face_anim.set_anim(anim)

    def set_image(self, image):
        self.image = image
