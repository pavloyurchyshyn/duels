from obj_properties.base_projectile import Projectile
from obj_properties.rect_form import Rectangle
from settings.window_settings import MAIN_SCREEN, SCREEN_W, SCREEN_H

from settings.visual_settings.effects_types import FIRE_TYPE
from common_things.camera import GLOBAL_CAMERA
from common_things.global_clock import GLOBAL_CLOCK


from pygame.draw import circle as draw_circle

from visual.transparent_circle_effect import TransparentCircle
from visual.visual_effects_controller import VisualEffectsController
from random import randrange, random, choice


class FireEffect(Projectile):
    EFFECT_TYPE = FIRE_TYPE

    FIRE_COLOR = [225, 225, 0]
    FIRE_COLOR_CHANGE = [-100, -255, 0]

    SPARKLE_COLORS = [255, 125, 0], [225, 225, 0]
    SPARKLE_COLOR_CHANGE = [-200, -255, 0]

    HEAD_COLOR = (255, 255, 255)

    speed_frequency = 10 * 0.1

    def __init__(self, x, y, angle=0,
                 speed=0,
                 live_time=None,

                 head_radius=10,
                 head_color=None,
                 head_line_width=0,

                 particle_creating_delay=0.1,
                 particle_size=30,
                 particle_size_scale=-1,
                 particle_speed=10,
                 particle_color=None,
                 particle_color_change=None,

                 sparkles=1,
                 sparkles_colors=None,
                 sparkles_color_change=None,
                 arena=Rectangle(0, 0, SCREEN_W, SCREEN_H),

                 **kwargs):

        super(FireEffect, self).__init__(x=x, y=y, speed=speed,
                                         angle=angle, arena=arena,
                                         round_clock=0, **kwargs)

        self._next_create = 0.5
        self._live_time = live_time
        self._screen = MAIN_SCREEN

        self._head_radius = head_radius
        self._head_color = head_color if head_color else self.HEAD_COLOR
        self._head_line_width = head_line_width

        self._particle_creating_delay = -particle_creating_delay # + particle_speed*self.speed_frequency
        self._particle_size = particle_size
        self._particle_size_scale = particle_size_scale
        self._particle_speed = particle_speed
        self._particle_color = particle_color if particle_color else self.FIRE_COLOR
        self._particle_color_change = particle_color_change if particle_color_change else self.FIRE_COLOR_CHANGE

        self._sparkles = sparkles
        self._sparkles_colors = sparkles_colors if sparkles_colors else self.SPARKLE_COLORS
        self._sparkles_color_change = sparkles_color_change if sparkles_color_change else self.SPARKLE_COLOR_CHANGE

        self._fire_particles = []
        self._position_rand_range = (-particle_size // 15, particle_size // 15)

    def update(self):
        self._update()

        if self._next_create < 0:
            self._next_create += GLOBAL_CLOCK.d_time
        else:
            self._next_create = self._particle_creating_delay
            x, y = self._position
            x += randrange(*self._position_rand_range)
            y += randrange(*self._position_rand_range)
            fire = TransparentCircle(x=x, y=y,
                                     size=self._particle_size,
                                     speed=self._particle_speed,
                                     size_scale=self._particle_size_scale,
                                     color=self.FIRE_COLOR.copy(),
                                     color_change=self.FIRE_COLOR_CHANGE,
                                     angle=self._angle + randrange(0, 360),
                                     round_clock=0,
                                     transparent=0,
                                     )

            self._fire_particles.append(fire)

            if self._sparkles and random() > 0.8:
                self._fire_particles.append(TransparentCircle(x=x, y=y,
                                                              size=5,
                                                              speed=self._particle_speed * 5,
                                                              angle=self._angle + randrange(-90, 90),
                                                              color=choice(self._sparkles_colors).copy(),
                                                              transparent=0,
                                                              color_change=self._sparkles_color_change,
                                                              size_scale=-.5,
                                                              ))

        for effect in self._fire_particles.copy():
            effect.update()
            if effect.dead:
                self._fire_particles.remove(effect)

        if self._live_time:
            self._live_time -= self._d_time

        # self.position = GLOBAL_MOUSE.pos

    def draw(self):
        # draw_circle(self._screen, (0, 255, 0), self.int_position, 5)
        for effect in reversed(self._fire_particles):
            effect.draw()

        x, y = self._position
        dx, dy = GLOBAL_CAMERA.camera

        if self._head_radius:
            draw_circle(self._screen, self._head_color, (x + dx, y + dy), self._head_radius, self._head_line_width)

    @staticmethod
    def alive_condition(self):
        if self._live_time:
            return self._live_time > 0
        else:
            return not self.out_of_arena()

    def __del__(self):
        for effect in self._fire_particles:
            VisualEffectsController.add_effect(effect)


class VioletFire(FireEffect):
    FIRE_COLOR = [255, 0, 255]
    FIRE_COLOR_CHANGE = [-200, -0, -200]

    SPARKLE_COLORS = [255, 0, 255], [255, 50, 255]
    SPARKLE_COLOR_CHANGE = [-200, -255, -255]

    HEAD_COLOR = (100, 0, 100)


class GreenBlueFire(FireEffect):
    FIRE_COLOR = [100, 255, 255]
    FIRE_COLOR_CHANGE = [-255, -200, -255]

    SPARKLE_COLORS = [100, 220, 255], [255, 220, 220]
    SPARKLE_COLOR_CHANGE = [-255, -255, -200]


class BlueFire(FireEffect):
    FIRE_COLOR = [100, 100, 255]
    FIRE_COLOR_CHANGE = [-255, -255, -255]

    SPARKLE_COLORS = [100, 100, 255], [200, 200, 255]
    SPARKLE_COLOR_CHANGE = [-255, -255, -100]


class GreenFire(FireEffect):
    FIRE_COLOR = [100, 255, 100]
    FIRE_COLOR_CHANGE = [-255, -200, -255]

    SPARKLE_COLORS = [100, 255, 100], [200, 255, 100]
    SPARKLE_COLOR_CHANGE = [-200, -255, -255]

    HEAD_COLOR = (0, 155, 0)
