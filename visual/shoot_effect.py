from obj_properties.base_projectile import Projectile
from obj_properties.rect_form import Rectangle
from settings.window_settings import MAIN_SCREEN, SCREEN_W, SCREEN_H
from common_things.camera import GLOBAL_CAMERA

from pygame.draw import polygon as draw_polygon
from pygame.draw import lines as draw_lines

from visual.visual_effects_controller import VisualEffectsController
from visual.diamond_effect import DiamondEffect
from math import cos, sin, radians

from random import choice


class ShootEffect:
    colors = (
        # [255, 100, 255, 255],
        [155, 55, 255],
        [255, 55, 155],
    )

    def __init__(self, x, y, arena=None, angle=0):
        for i in range(3):
            VisualEffectsController.add_effect(DiamondEffect(x=x, y=y,
                                                             angle=angle + radians(i),
                                                             speed=1000,
                                                             tail_len=10,
                                                             head_len=50,
                                                             width_len=5,
                                                             color=choice(self.colors).copy(),
                                                             scale_per_second=[2, 2, 3],
                                                             color_change=[250, 250, 250],
                                                             fill_form=1,
                                                             arena=arena,
                                                             ))
