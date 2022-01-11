from settings.window_settings import SCREEN_W, SCREEN_H, MAIN_SCREEN
from obj_properties.rect_form import Rectangle
from common_things.global_round_parameters import GLOBAL_ROUND_PARAMETERS
from common_things.camera import GLOBAL_CAMERA
from common_things.common_functions import get_angle_between_dots
from pygame import draw
from objects.ball import Ball


class BallArrow:
    GLOBAL_ROUND_PARAMETERS = GLOBAL_ROUND_PARAMETERS

    def __init__(self):
        self._ball: Ball = None
        self._screen_rect = Rectangle(0, 0, SCREEN_W, SCREEN_H)
        self._angle = 0.
        self._arrow_img = None
        self._arrow_position = None
        self._img_size = (10, 10)

    def unfollow_ball(self):
        self._ball = None

    def follow_ball(self, ball):
        self._ball = ball

    def update(self):
        if self._ball:
            ball_x_pos, ball_y_pos = self._ball._center
            dx, dy = GLOBAL_CAMERA.camera
            ball_pos_on_screen = [ball_x_pos + dx, ball_y_pos + dy]
            if not self._screen_rect.collide_point(ball_pos_on_screen):
                self._angle = get_angle_between_dots(self._screen_rect.center, ball_pos_on_screen)

                if ball_pos_on_screen[0] > self._screen_rect.size_x:
                    ball_pos_on_screen[0] = self._screen_rect.size_x - self._img_size[0]
                elif ball_pos_on_screen[0] < 0:
                    ball_pos_on_screen[0] = 1 + self._img_size[0]

                if ball_pos_on_screen[1] > self._screen_rect.size_y:
                    ball_pos_on_screen[1] = self._screen_rect.size_y - self._img_size[1]
                elif ball_pos_on_screen[1] < 0:
                    ball_pos_on_screen[1] = 1 + self._img_size[1]

                self._arrow_position = ball_pos_on_screen

            else:
                self._arrow_position = None

    def draw(self):
        if self._arrow_position:
            draw.circle(MAIN_SCREEN, (255, 255, 0), self._arrow_position, 10)
            draw.circle(MAIN_SCREEN, (0, 0, 0), self._arrow_position, 10, 1)
