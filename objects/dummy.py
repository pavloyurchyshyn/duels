from player.base_player import BasePlayer
from obj_properties.physic_body import PhysicalObj
from settings.players_settings.player_settings import PLAYER_SIZE
from pygame import transform
from pygame.draw import circle
from math import degrees
from common_things.global_clock import ROUND_CLOCK
from settings.global_parameters import test_draw_status_is_on


class Dummy(BasePlayer, PhysicalObj):
    def __init__(self, x, y,
                 arena,
                 size=PLAYER_SIZE,
                 **kwargs):
        super().__init__(x, y, size=size,
                         arena=arena,
                         player_skin={'body': (100, 100, 100), 'face': (0, 0, 0)},
                         load_images=True, **kwargs)
        PhysicalObj.__init__(self, 1.1)
        self.face_anim.change_animation('rage')

    def update(self, *args, **kwargs):
        time_d = ROUND_CLOCK.d_time
        self._d_time = time_d
        self._time += time_d
        self.use_self_force(1)
        self.check_for_bullets_interaction()
        self.check_for_spells_interaction()
        self.health_points_text.change_pos(self._center[0], self._center[1] + self._size)
        d = self.damaged
        if d:
            self.health_points_text.change_text(d)

        self.face_anim.update(d_time=time_d, position=self._center, angle=self._angle)

    def _draw(self) -> None:
        dx, dy = self.camera.camera

        x0, y0 = self._center

        main_screen = self.MAIN_SCREEN

        img_copy = transform.rotate(self.image, -degrees(self._angle))
        main_screen.blit(img_copy, (x0 - img_copy.get_width() // 2 + dx, y0 - img_copy.get_height() // 2 + dy))

        if test_draw_status_is_on():
            for dot in self._dots:
                circle(main_screen, (255, 0, 0), (dot[0] + dx, dot[1] + dy), 3)

        # circle(main_screen,
        #        self.color['body'],
        #        (self._hands_endpoint[0] + dx, self._hands_endpoint[1] + dy),
        #        5)

        self.face_anim.draw(dx, dy)
        self.health_points_text.draw(dx, dy)

        for item in self._weapon.values():
            if item:
                item.draw()
