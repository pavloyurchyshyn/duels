from UI.UI_base.menu_UI import MenuUI
from UI.UI_buttons.test_draw import TEST_DRAW_BUTTON

from common_things.global_keyboard import GLOBAL_KEYBOARD
from common_things.global_clock import GLOBAL_CLOCK
from common_things.common_functions import get_angle_between_dots

from settings.colors import HALF_EMPTY
from settings.window_settings import SCREEN_H, SCREEN_W, HALF_SCREEN_W, HALF_SCREEN_H, MAIN_SCREEN
from settings.UI_setings.menus_settings.main_menu import MAIN_MENU_BUTTONS, exit_warning, \
    activate_exit_warning_message, deactivate_exit_warning_message
from settings.global_parameters import pause_available, pause_step
from settings.game_stages_constants import MAIN_MENU_STAGE

from visual.visual_effects_controller import VisualEffectsController
from visual.diamond_effect import DiamondEffect
from visual.transparent_circle_effect import TransparentCircle
from visual.fire import FireEffect, VioletFire, GreenFire, GreenBlueFire, BlueFire
from visual.tornado_effect import Tornado
from visual.growing_line import GrowingLine
from random import randrange, random, choice, randint
from math import cos

from common_things.global_mouse import GLOBAL_MOUSE

VisualEffectsController.add_effect(FireEffect(HALF_SCREEN_H / 5, 100, speed=110))
VisualEffectsController.add_effect(VioletFire(HALF_SCREEN_H / 5, 200, speed=110))
VisualEffectsController.add_effect(GreenFire(HALF_SCREEN_H / 5, 300, speed=110))
VisualEffectsController.add_effect(GreenBlueFire(HALF_SCREEN_H / 5, 400, speed=110))
VisualEffectsController.add_effect(BlueFire(HALF_SCREEN_H / 5, 500, speed=110))


class MainMenu(MenuUI):
    def __init__(self):
        super().__init__(buttons=MAIN_MENU_BUTTONS,
                         buttons_objects=[TEST_DRAW_BUTTON, ],
                         name=MAIN_MENU_STAGE, surface=MAIN_SCREEN)
        self.create_buttons()
        self._fade_surface = self.get_surface(transparent=True)
        self._fade_surface.fill(HALF_EMPTY)
        self._fade_surface.convert_alpha()
        self.add_elements_to_controller(*self._elements, enter_focus=self.start)
        self.last_spawn = 1

    def spawn_particle(self):
        if self.last_spawn < 0:
            self.last_spawn += GLOBAL_CLOCK.d_time
        else:
            self.last_spawn = -0.1
            if randint(0, 1):
                x = choice((1, SCREEN_W))
                y = randrange(1, SCREEN_H)
            else:
                x = randrange(1, SCREEN_W)
                y = choice((SCREEN_H, 1))

            angle = get_angle_between_dots((x, y), (HALF_SCREEN_W, HALF_SCREEN_H) )
            r, g = randrange(0, 255), randrange(0, 255)
            VisualEffectsController.add_effect(DiamondEffect(x, y,
                                                             speed=200, angle=angle,
                                                             color=[r, g, 255, 255],
                                                             scale_per_second=(0.4, 0.4, 0.4),
                                                             fill_form=0,
                                                             color_change=[-r / 2, -g / 2, -100, 0],
                                                             ))

            # VisualEffectsController.add_effect(TransparentCircle(x, y, angle=angle, color=[155, 155, 155], leave_tail=1, size_scale=-1))

            # angle = get_angle_between_dots((HALF_SCREEN_W, HALF_SCREEN_H), (HALF_SCREEN_W, 0))
            # VisualEffectsController.add_effect(GrowingLine(HALF_SCREEN_W + 200*cos(GLOBAL_CLOCK.time), 0, angle=angle))

    def update(self):
        VisualEffectsController.update()

        for button in self._elements:
            button.update()

        self.spawn_particle()

        if GLOBAL_KEYBOARD.ESC and pause_available() and not exit_warning():
            pause_step()
            activate_exit_warning_message()
            self.drop_focused()

        elif GLOBAL_KEYBOARD.ESC and pause_available() and exit_warning():
            pause_step()
            deactivate_exit_warning_message()
            self.drop_focused()

        if self.click():
            xy = self.GLOBAL_MOUSE.pos
            if not exit_warning():
                for button in self._buttons:
                    button.click(xy=xy)
                    if button.clicked:
                        break

            elif not self._exit_yes.click(xy):
                deactivate_exit_warning_message()

    def draw(self, dx=0, dy=0):
        # self._screen.blit(self._surface, (self._x_pic + dx, self._y_pic + dy))
        self._screen.fill((0, 0, 0, 255))
        if self._picture:
            self._screen.blit(self._picture, (self.x0 + dx, self.y0 + dy))
        VisualEffectsController.draw()

        for element in self._elements:
            element.draw(dx, dy)

        if exit_warning():
            self.surface.blit(self._fade_surface, (0, 0))

            self._exit_no.draw()
            self._exit_yes.draw()

    def _update(self):
        pass


MAIN_MENU_UI = MainMenu()
