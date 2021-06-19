from UI.UI_base.menu_UI import MenuUI
from UI.UI_buttons.test_draw import TEST_DRAW_BUTTON

from settings.colors import BLACK, HALF_EMPTY

from settings.UI_setings.menus_settings.main_menu import MAIN_MENU_BUTTONS


class MainMenu(MenuUI):
    def __init__(self):
        super().__init__(buttons=MAIN_MENU_BUTTONS, buttons_objects=[TEST_DRAW_BUTTON, ])
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
                    return

                else:
                    self._exit_yes.make_inactive()
                    self._exit_yes.make_invisible()
                    self._exit_no.make_inactive()
                    self._exit_no.make_invisible()
                    self._exit_warning = 0
                    self._surface.fill(BLACK)

    def draw(self, dx=0, dy=0):
        self._draw(dx, dy)
        if self._exit_warning:
            self.surface.blit(self._fade_surface, (0, 0))
            self._exit_no.draw()
            self._exit_yes.draw()

    def _update(self):
        pass


MAIN_MENU_UI = MainMenu()
