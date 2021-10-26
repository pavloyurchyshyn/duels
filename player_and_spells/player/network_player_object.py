from player_and_spells.player.base_player import BasePlayer
from common_things.global_clock import ROUND_CLOCK
from obj_properties.objects_data_creator import objects_data_creator
from settings.default_keys import SELF_DAMAGE


class NetworkPlayerObject(BasePlayer):
    def __init__(self, x, y,
                 arena,
                 team=None,
                 **kwargs):
        super().__init__(x=x, y=y, team=team, arena=arena, **kwargs)

    def update(self, commands=(), mouse_buttons=(0, 0, 0), mouse_pos=None):
        time_d = ROUND_CLOCK.d_time
        self._d_time = time_d
        self._time += time_d

        self.update_effects(time_d)
        self.make_step(commands)

        self.update_hands_endpoints()

        if mouse_buttons[0]:
            self._arena.add_object(objects_data_creator(name='simple_bullet',
                                                        data={
                                                            'x': self._hands_endpoint[0],
                                                            'y': self._hands_endpoint[1],
                                                            'angle': self._angle,
                                                        }))

        if SELF_DAMAGE in commands:
            self.damage(5)

        self.check_for_bullets_damage()


