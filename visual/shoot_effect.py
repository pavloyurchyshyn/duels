from visual.base.visual_effects_controller import VisualEffectsController
from visual.base.diamond_effect import DiamondEffect
from math import radians

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
