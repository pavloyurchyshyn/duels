from UI.UI_base.menu_UI import MenuUI
from UI.UI_buttons.test_draw import TEST_DRAW_BUTTON

from common_things.global_keyboard import GLOBAL_KEYBOARD

from settings.UI_setings.menus_settings.round_pause import ROUND_PAUSE_BUTTONS, \
    PAUSE_MAIN_SCREEN_COPY

from common_things.stages import Stages
from settings.game_stages_constants import ROUND_PAUSE_STAGE

set_main_menu_stage = Stages().set_main_menu_stage


class RoundPause(MenuUI):
    Pause_back_color = (0, 0, 0, 100)

    def __init__(self):
        super().__init__(buttons=ROUND_PAUSE_BUTTONS, buttons_objects=[TEST_DRAW_BUTTON, ],
                         background_color=self.Pause_back_color, transparent=1, name=ROUND_PAUSE_STAGE)
        self.create_buttons()
        self._exit_warning = False

        self._fade_surface = self.get_surface(transparent=True)
        self._fade_surface.fill((0, 0, 0, 150))
        self._fade_surface.convert_alpha()

    def activate_exit_buttons(self):
        self._exit_yes.make_active()
        self._exit_yes.make_visible()
        self._exit_no.make_active()
        self._exit_no.make_visible()

        for button in self._buttons:
            if button in (self._exit_yes, self._exit_no, TEST_DRAW_BUTTON):
                continue
            button.make_inactive()

        self._exit_warning = 1
        self.draw_round()

        self.surface.blit(self._fade_surface, (0, 0))

    def deactivate_exit_buttons(self):
        self._exit_yes.make_inactive()
        self._exit_yes.make_invisible()
        self._exit_no.make_inactive()
        self._exit_no.make_invisible()

        for button in self._buttons:
            if button in (self._exit_yes, self._exit_no, TEST_DRAW_BUTTON):
                continue
            button.make_active()

        self._exit_warning = 0
        self._surface.fill((0, 0, 0, 0))
        self.draw_round()

    def draw_round(self, fill=1):
        self._surface.blit(PAUSE_MAIN_SCREEN_COPY, (0, 0))
        if fill:
            self.surface.blit(self._fade_surface, (0, 0))

    def update(self):
        if GLOBAL_KEYBOARD.ESC and self._exit_warning:
            self.deactivate_exit_buttons()

        for button in self._elements:
            button.update()

        if self.click():
            xy = self.GLOBAL_MOUSE.pos
            if not self._exit_warning:
                for button in self._buttons:
                    button.click(xy=xy)
                    if button.clicked:
                        break

                self._exit.click(xy=xy)
                if self._exit.clicked:
                    self.activate_exit_buttons()
            else:
                if self._exit_yes.click(xy):
                    self.deactivate_exit_buttons()
                    set_main_menu_stage()

                else:
                    self.deactivate_exit_buttons()

    # def update_main_screen(self):
    #     PAUSE_MAIN_SCREEN_COPY = MAIN_SCREEN.copy()

    def draw(self, dx=0, dy=0):
        self._draw(dx, dy)
        if self._exit_warning:
            self._exit_no.draw()
            self._exit_yes.draw()


ROUND_PAUSE_UI = RoundPause()
