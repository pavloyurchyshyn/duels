from UI.UI_base.menu_UI import MenuUI

from settings.colors import HALF_EMPTY
from settings.UI_setings.menus_settings.round_pause import ROUND_PAUSE_BUTTONS
from settings.global_parameters import GLOBAL_SETTINGS
from settings.game_stages import CURRENT_STAGE, ROUND_S, MAIN_MENU_S
from UI.UI_buttons.test_draw import TEST_DRAW_BUTTON


class RoundPause(MenuUI):
    Pause_back_color = (0, 0, 0, 100)

    def __init__(self):
        super().__init__(buttons=ROUND_PAUSE_BUTTONS, buttons_objects=[TEST_DRAW_BUTTON, ],
                         background_color=self.Pause_back_color, transparent=1)
        self.create_buttons()
        self._exit_warning = False

        self._fade_surface = self.get_surface(transparent=True)
        self._fade_surface.fill(HALF_EMPTY)
        self._fade_surface.convert_alpha()

    def update(self):
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
                    self._exit_yes.make_active()
                    self._exit_yes.make_visible()
                    self._exit_no.make_active()
                    self._exit_no.make_visible()
                    self._exit_warning = 1
            else:
                if self._exit_yes.click(xy):
                    self._exit_yes.make_inactive()
                    self._exit_yes.make_invisible()
                    self._exit_no.make_inactive()
                    self._exit_no.make_invisible()
                    self._exit_warning = 0
                    self._surface.fill(self.Pause_back_color)

                    GLOBAL_SETTINGS[CURRENT_STAGE] = MAIN_MENU_S
                    return

                else:
                    self._exit_yes.make_inactive()
                    self._exit_yes.make_invisible()
                    self._exit_no.make_inactive()
                    self._exit_no.make_invisible()
                    self._exit_warning = 0
                    self._surface.fill(self.Pause_back_color)

    def draw(self, dx=0, dy=0):
        self._draw(dx, dy)
        if self._exit_warning:
            # self.surface.blit(self._fade_surface, (0, 0))
            self._exit_no.draw()
            self._exit_yes.draw()


ROUND_PAUSE_UI = RoundPause()
