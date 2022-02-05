from visual.base.diamond_effect import DiamondEffect
from visual.base.visual_effects_controller import VisualEffectsController
from math import cos, sin, radians
from random import random

r90 = radians(90)
r25 = radians(25)
effects_number = 3


def base_hit_effect_func(self, x, y, angle):
    effect = DiamondEffect(x=x, y=y, angle=angle, speed=300,
                           live_time=0.3, scale_per_second=(1, 1, 1), fill_form=1,
                           head_len=50, tail_len=50, width_len=2 + 5 * random())
    VisualEffectsController.add_effect(effect)

    for i in range(3):
        add_angle = r90 + (0.5 if random() > 0.5 else -0.5) * random()
        live_time = 0.5 * random() + 0.25 * random()
        tail_len = 25 + 25 * random()
        speed = 100 + 200 * random()

        effect = DiamondEffect(x=x, y=y, angle=angle + add_angle, speed=speed, round_clock=1,
                               live_time=live_time, scale_per_second=(1, 1, 1), fill_form=1,
                               head_len=50, tail_len=tail_len, width_len=2 + 5 * random())
        VisualEffectsController.add_effect(effect)

        effect = DiamondEffect(x=x, y=y, angle=angle - add_angle, speed=speed, round_clock=1,
                               live_time=live_time, scale_per_second=(1, 1, 1), fill_form=1,
                               head_len=50, tail_len=tail_len, width_len=2 + 5 * random())
        VisualEffectsController.add_effect(effect)

        add_angle = r25 + (0.5 if random() > 0.5 else -0.5) * random()
        tail_len = 55 + 25 * random()

        effect = DiamondEffect(x=x, y=y, angle=angle + add_angle, speed=speed, round_clock=1,
                               live_time=live_time, scale_per_second=(1, 1, 1), fill_form=1,
                               head_len=50, tail_len=tail_len, width_len=2 + 5 * random())
        VisualEffectsController.add_effect(effect)
        effect = DiamondEffect(x=x, y=y, angle=angle - add_angle, speed=speed, round_clock=1,
                               live_time=live_time, scale_per_second=(1, 1, 1), fill_form=1,
                               head_len=50, tail_len=tail_len, width_len=2 + 5 * random())

        VisualEffectsController.add_effect(effect)
