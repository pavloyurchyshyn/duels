from UI.UI_base.menu_UI import MenuUI

from settings.colors import BLACK, HALF_EMPTY

from settings.UI_setings.menus_settings.multiplayer import MULTIPLAYER_BUTTONS, SERVER_PASSWORD


class Multiplayer(MenuUI):
    def __init__(self):
        super().__init__(buttons=MULTIPLAYER_BUTTONS)
        self.create_buttons()
        self._exit_warning = False
        self._fade_surface = self.get_surface(transparent=True)
        self._fade_surface.fill(HALF_EMPTY)
        self._fade_surface.convert_alpha()
        self._server_pswrd = SERVER_PASSWORD

    def update(self):
        self._server_pswrd.update()

        for button in self._elements:
            button.update()

        if self.click():
            xy = self.GLOBAL_MOUSE.pos
            for button in self._buttons:
                button.click(xy)

    def draw(self, dx=0, dy=0):
        self._draw(dx, dy)
        if self._exit_warning:
            self.surface.blit(self._fade_surface, (0, 0))

        self._server_pswrd.draw(dx, dy)

    def _update(self):
        pass


MULTIPLAYER_UI = Multiplayer()
