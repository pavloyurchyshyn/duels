from pygame.draw import line, circle, polygon
from settings.window_settings import MAIN_SCREEN
from common_things.global_clock import GLOBAL_CLOCK, ROUND_CLOCK
from common_things.camera import GLOBAL_CAMERA
from common_things.common_functions import get_angle_between_dots
from math import cos, sin


class FollowingLine:
    def __init__(self, x, y, g_clock=1, max_tail_w=20, color=(255, 255, 255)):
        self.x, self.y = x, y
        self._joints = []
        # join: {'x': 0, 'y': 0, 'alive_time': 1}

        self._clock = GLOBAL_CLOCK if g_clock else ROUND_CLOCK
        self._color = color

        self._next_join_create = 1
        self._join_create_cd = -0.03
        self._join_alive_time = 0.5
        self._prev_pos = self.x, self.y
        self.max_tail_w = max_tail_w
        self._first_tail_w = self.max_tail_w / 2

    def update(self, x, y):
        self.x, self.y = x, y
        d_time = self._clock.d_time
        if self._next_join_create <= 0:
            self._next_join_create += d_time
        elif self._prev_pos != (self.x, self.y):
            self._next_join_create = self._join_create_cd
            self.create_join()

        self.update_joints(d_time)
        self._prev_pos = self.x, self.y

    def create_join(self):
        if len(self._joints) > 1:
            angle = get_angle_between_dots((self.x, self.y), (self._joints[1]['x'], self._joints[1]['y'])) + 1.5707963267948966
            self._joints[1]['angle'] = angle
        else:
            angle = 0.001

        self._joints.append({'x': self.x, 'y': self.y, 'alive_time': self._join_alive_time, 'angle': angle})

    def update_joints(self, d_time):
        for joint in self._joints.copy():
            joint['alive_time'] -= d_time
            if joint['alive_time'] < 0:
                self._joints.remove(joint)

    def draw(self):
        dx, dy = GLOBAL_CAMERA.camera

        if len(self._joints) > 1:
            polygon_ = []
            for joint in self._joints:
                tail_w = self.max_tail_w * (joint['alive_time'] / self._join_alive_time)
                if self._joints.index(joint) == len(self._joints)-1:
                    tail_w = self._first_tail_w
                x0 = joint['x'] + cos(joint['angle']) * tail_w + dx
                x1 = joint['x'] - cos(joint['angle']) * tail_w + dx
                y0 = joint['y'] + sin(joint['angle']) * tail_w + dy
                y1 = joint['y'] - sin(joint['angle']) * tail_w + dy
                polygon_.append((x0, y0))
                # polygon_.append((x1, y1))
                polygon_.insert(0, (x1, y1))

            polygon(MAIN_SCREEN, self._color, polygon_)

        # pre_pos = self.x + dx, self.y + dy
        # for joint in reversed(self._joints):
        #     cur_pos = joint['x'] + dx, joint['y'] + dy
        #     line(MAIN_SCREEN, (255, 0, 0), pre_pos, cur_pos, 3)
        #     circle(MAIN_SCREEN, (0, 255, 0), cur_pos, 2)
        #     pre_pos = cur_pos


