from player_and_spells.player.base_player import BasePlayer
from common_things.global_clock import ROUND_CLOCK
from obj_properties.objects_data_creator import objects_data_creator
from common_things.common_objects_lists_dicts import BULLETS_LIST


class NetworkPlayerObject(BasePlayer):
    def __init__(self, x, y,
                 arena,
                 team=None,
                 **kwargs):
        super().__init__(x=x, y=y, team=team, arena=arena, **kwargs)

        self.bullets_list = BULLETS_LIST

    def update(self, commands=(), mouse_buttons=(0, 0, 0), mouse_pos=None):
        time_d = ROUND_CLOCK.d_time
        self._d_time = time_d
        self._time += time_d

        self.make_step(commands)

        self.update_hands_endpoints()

        if mouse_buttons[0]:
            self._arena.add_object(objects_data_creator(name='simple_bullet',
                                                        data={
                                                            'x': self._hands_endpoint[0],
                                                            'y': self._hands_endpoint[1],
                                                            'angle': self._angle,
                                                        }))

        self.check_for_bullets_damage()

    def check_for_bullets_damage(self):
        for bullet in self.bullets_list:
            if self.collide_point(bullet.position):
                self.damage(bullet.damage)
                bullet.kill()

    @property
    def health_points(self):
        return self._health_points

    @health_points.setter
    def health_points(self, health_points):
        self._health_points = health_points
