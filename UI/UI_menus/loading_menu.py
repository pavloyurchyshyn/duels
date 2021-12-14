from UI.UI_base.menu_UI import MenuUI
from settings.UI_setings.menus_settings.loading import PLAYER_PIC
from settings.game_stages_constants import LOADING_STAGE
from visual.fire import GreenFire, FireEffect, BlueFire, VioletFire
from visual.tornado_effect import Tornado
from visual.visual_effects_controller import VisualEffectsController
from math import sin, cos, radians
from obj_properties.rect_form import Rectangle
from settings.window_settings import SCREEN_W, SCREEN_H
from common_things.global_clock import GLOBAL_CLOCK


class Loading_menu(MenuUI):
    def __init__(self):
        super().__init__(name=LOADING_STAGE)
        self.create_buttons()

        self._effects = []

        self.x0, self.y0 = SCREEN_W * 0.9, SCREEN_H * 0.85
        self._radius = SCREEN_W * 0.05

        self.__angles = (radians(0), radians(90), radians(180), radians(270))
        for angle, fire in zip(self.__angles, (GreenFire, FireEffect, BlueFire, VioletFire)):
            x = self.x0 + cos(angle) * 100
            y = self.y0 + sin(angle) * 100

            d = fire(x=x, y=y,
                     arena=Rectangle(0, 0, SCREEN_W, SCREEN_H),
                     angle=angle,
                     speed=0,
                     # angle_change_per_second=10,
                     particle_creating_delay=0.05,
                     )
            self._effects.append(d)

    def update(self):
        for angle, effect in zip(self.__angles, self._effects):

            x = self.x0 + cos(GLOBAL_CLOCK.time * 1.5 + angle) * self._radius
            y = self.y0 + sin(GLOBAL_CLOCK.time * 1.5 + angle) * self._radius

            effect.position = x, y
            if effect not in VisualEffectsController.effects():
                VisualEffectsController.add_effect(effect)

        PLAYER_PIC.update()

    def draw(self, dx=0, dy=0):
        self._draw(dx, dy)
        PLAYER_PIC.draw()
        VisualEffectsController.draw()


LOADING_MENU_UI = Loading_menu()
