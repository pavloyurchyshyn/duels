from visual.base.diamond_effect import DiamondEffect
from visual.base.transparent_circle_effect import TransparentCircle
from visual.base.visual_effects_controller import VisualEffectsController
from math import radians, cos, sin
from random import random, randrange
from pygame.draw import circle as draw_circle
from pygame.draw import polygon as draw_polygon


def player_hit_effect(x, y, angle, arena):
    surface = arena.surface
    for i in range(-16, 15, 15):
        draw_circle(surface, (155, 50, 50),
                    (x + (1 + 25*random())*cos(angle+radians(i)*random()), y + (1 + 20*random()*sin(angle+radians(i)*random()))),
                    5 * random())

        for t in range(1, int(5*random())):
            draw_polygon(surface, (155, 50, 50), DiamondEffect(x, y, without_camera=1,
                                                               tail_len=1 + 35 * random(),
                                                               head_len=3 + 5 * random(),
                                                               width_len=1 + 5 * random(),
                                                               angle=angle + random() * radians(randrange(-45, 45))).points)
