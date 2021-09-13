from obj_properties.circle_form import Circle
from settings.players_settings.player_settings import *
from settings.global_parameters import GLOBAL_SETTINGS
from abc import abstractmethod
from settings.default_keys import UP_C, LEFT_C, RIGHT_C, DOWN_C, SPRINT_C, WEAPON_1_C, WEAPON_2_C, WEAPON_3_C
from math import atan2, cos, sin
from world_arena.base.arena_cell_obj import ArenaCellObject


class BasePlayer(Circle):
    PLAYER_HP = PLAYER_HEALTH_POINTS
    PLAYER_SPEED = PLAYER_SPEED
    PLAYER_SPRINT_SPEED = PLAYER_SPRINT_SPEED
    PLAYER_GLIDE_K = PLAYER_GLIDE_K
    PLAYER_HANDS_SIZE = PLAYER_HANDS_SIZE

    def __init__(self, x, y,
                 arena: ArenaCellObject,
                 team=None,
                 size=PLAYER_SIZE,
                 **kwargs):
        super().__init__(x, y, size, dots_angle=True)
        self._arena: ArenaCellObject = arena
        self.team = team
        self._angle = 0.0
        self.global_settings = GLOBAL_SETTINGS

        self._full_health_points = kwargs.get('health_points', BasePlayer.PLAYER_HP)
        self._health_points = self._full_health_points

        self.speed = kwargs.get('speed', BasePlayer.PLAYER_SPEED)
        self.sprint_speed = kwargs.get('sprint_speed', BasePlayer.PLAYER_SPRINT_SPEED)

        self.spawn_position = kwargs.get('spawn_position', (x, y))

        self._time = 0.000000001
        self._d_time = 0.00000001

        self._inventory = {
            1: kwargs.get(WEAPON_1_C, None),
            2: kwargs.get(WEAPON_2_C, None),
            3: kwargs.get(WEAPON_3_C, None),
        }
        self._damaged = 0
        self._hands_endpoint = [0, 0]

    def update_hands_endpoints(self):
        self._hands_endpoint[0] = self._center[0] + cos(self._angle) * self.PLAYER_HANDS_SIZE
        self._hands_endpoint[1] = self._center[1] + sin(self._angle) * self.PLAYER_HANDS_SIZE

    def make_step(self, commands) -> bool:
        """
        @return: True if position changed
        """
        step_speed = self.sprint_speed if SPRINT_C in commands else self.speed
        step_speed = step_speed * self._d_time

        x_step = 0
        if RIGHT_C in commands:
            x_step += step_speed
        if LEFT_C in commands:
            x_step -= step_speed

        y_step = 0
        if UP_C in commands:
            y_step -= step_speed
        if DOWN_C in commands:
            y_step += step_speed

        if x_step != 0 or y_step != 0:
            x, y = self._center
            new_x, new_y = x + x_step, y + y_step
            self._change_position((new_x, new_y))
            return True

        return False

    def rotate_to_cursor(self, mouse_pos: tuple, camera_x_position=0, camera_y_position=0) -> bool:
        """
        :return: True if angle changed
        """
        x_mouse_position, y_mouse_position = mouse_pos
        x_center_position, y_center_position = self._center

        x_center_position += camera_x_position
        y_center_position += camera_y_position

        d_x = 0.00001 if x_mouse_position - x_center_position == 0 else x_mouse_position - x_center_position
        d_y = 0.00001 if y_mouse_position - y_center_position == 0 else y_mouse_position - y_center_position

        old_angle = self._angle
        self._angle = atan2(d_y, d_x)

        return self._angle != old_angle

    def revise(self):
        self._health_points = self._full_health_points

    def damage(self, damage):
        self._health_points -= damage
        self._damaged += damage

    @property
    def damaged(self):
        d = self._damaged
        self._damaged = 0
        return d

    @abstractmethod
    def update(self, commands=(), mouse_buttons=(0, 0, 0), mouse_pos=None):
        raise NotImplementedError

    @property
    def position(self):
        return self._center

    @position.setter
    def position(self, pos):
        if pos:
            self._change_position(pos)

    @property
    def full_health_points(self):
        return self._full_health_points

    @full_health_points.setter
    def full_health_points(self, hp):
        self._full_health_points = hp

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        if value:
            self._angle = value

    @property
    def alive(self):
        return self._health_points > 0

    @property
    def dead(self):
        return self._health_points <= 0
