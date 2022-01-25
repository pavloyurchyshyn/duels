from obj_properties.circle_form import Circle
from obj_properties.img_lazy_load import OnePictureLazyLoad, AdditionalLazyLoad
from obj_properties.physic_body import PhysicalObj
from settings.objects_settings.ball_settings import *
from world_arena.base.arena_cell_obj import ArenaCellObject
from common_things.camera import GLOBAL_CAMERA
from common_things.global_clock import ROUND_CLOCK
from common_things.common_objects_lists_dicts import SPELLS_LIST, BULLETS_LIST, MELEE_HITS_LIST
from settings.global_parameters import test_draw_status_is_on, its_client_instance


class Ball(Circle, PhysicalObj, OnePictureLazyLoad, AdditionalLazyLoad):

    def __init__(self, start_pos, arena: ArenaCellObject, size=BALL_DEFAULT_R):
        x, y = start_pos
        super().__init__(x, y, R=size)
        PhysicalObj.__init__(self, f_coef=1)
        OnePictureLazyLoad.__init__(self, size=(size, size))

        self._arena = arena
        self._start_pos = start_pos
        self._last_hit_player = None
        self._line_effect = None

        AdditionalLazyLoad.__init__(self, client_inst=its_client_instance())

    def additional_lazy_load(self):
        from visual.following_line import FollowingLine
        self._line_effect = FollowingLine(*self._center, max_tail_w=self._size, color=(105, 0, 255, 100))

    def reload(self):
        self._change_position(self._start_pos, 1)
        self.stop()

    def reverse_vertical(self):
        self._velocity.y = -self._velocity.y

    def reverse_horizontal(self):
        self._velocity.x = -self._velocity.x

    def update(self):
        self.check_for_bullet_intersection()
        self.check_for_spells_intersection()
        self.check_for_melee_hit_intersection()

        if self._velocity:
            d_time = ROUND_CLOCK.d_time
            self._velocity.mul_k(1 - self._f_coef * d_time)
            x, y = self._center

            new_x = x + self._velocity.x * d_time
            new_y = y + self._velocity.y * d_time

            self._change_position([new_x, new_y], 1)

            collided = 0
            if self._arena._exit_borders['top'].collide(self) or self._arena._exit_borders['bot'].collide(self):
                self._velocity.y = -self._velocity.y
                collided = 1

            if self._arena._exit_borders['left'].collide(self) or self._arena._exit_borders['right'].collide(self):
                self._velocity.x = -self._velocity.x

                collided = 1

            if collided and self._velocity.dist < self.h_size:
                self._velocity.mul_k(2)

            if self._arena.check_for_exit((new_x, new_y)):
                self._change_position([x, y], 1)

        if self._line_effect:
            self._line_effect.update(*self._center)

    def check_for_bullet_intersection(self):
        for bullet in BULLETS_LIST:
            if bullet.alive and self.collide(bullet):
                bullet.interact_with_object(self)
                self.set_last_hit_player(bullet.owner)

    def check_for_melee_hit_intersection(self):
        for hit in MELEE_HITS_LIST:
            if self.collide(hit):
                hit.interact_with_object(self)

    def check_for_spells_intersection(self):
        for spell in SPELLS_LIST:
            if spell.alive and self.collide(spell):
                spell.interact_with_object(self)
                self.set_last_hit_player(spell.owner)

    def set_last_hit_player(self, player):
        self._last_hit_player = player

    def draw(self):
        if self.CLIENT_INSTANCE:
            x, y = self._center
            dx, dy = GLOBAL_CAMERA.camera

            if self._line_effect:
                self._line_effect.draw()

            self.DRAW_CIRCLE(self.MAIN_SCREEN, (100, 100, 255), (x + dx, y + dy), self._size)
            self.DRAW_CIRCLE(self.MAIN_SCREEN, (50, 50, 155), (x + dx, y + dy), self._size, 2)

            if test_draw_status_is_on():
                for (dot_x, dot_y) in self._dots:
                    self.DRAW_CIRCLE(self.MAIN_SCREEN, (255, 255, 0), (dot_x + dx, dot_y + dy), 3)

    def damage(self, damage):
        pass
