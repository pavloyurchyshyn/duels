from visual.base.visual_effects_controller import VisualEffectsController
from visual.base.transparent_circle_effect import TransparentCircle
from visual.base.diamond_effect import DiamondEffect
from math import radians
from random import random

r5 = radians(10)


def bullet_death_effect(self, x, y, angle):
    color = [230+25*random(), 100+155*random(), 0]
    add_angle = 0.5*random() - 0.5 * random()
    VisualEffectsController.add_effect(TransparentCircle(x=x, y=y, speed=200, color=color.copy(), angle=angle,
                                                         size=10, size_scale=10,
                                                         circle_width=5,
                                                         circle_width_scale=-2))

    VisualEffectsController.add_effect(DiamondEffect(x=x, y=y, angle=angle - r5, speed=300, color=color.copy(),
                                                     live_time=0.3, scale_per_second=(1, 1, 1), fill_form=1,
                                                     head_len=15, tail_len=30, width_len=2))

    VisualEffectsController.add_effect(DiamondEffect(x=x, y=y, angle=angle + add_angle, speed=300, color=color.copy(),
                                                     color_change=[0, 0, 555],
                                                     live_time=0.3, scale_per_second=(1, 1, 1), fill_form=1,
                                                     head_len=50, tail_len=50, width_len=4))

    VisualEffectsController.add_effect(DiamondEffect(x=x, y=y, angle=angle + r5, speed=300, color=color.copy(),
                                                     live_time=0.3, scale_per_second=(1, 1, 1), fill_form=1,
                                                     head_len=15, tail_len=30, width_len=2))
