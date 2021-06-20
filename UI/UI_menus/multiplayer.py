from UI.UI_base.menu_UI import MenuUI

from settings.colors import BLACK, HALF_EMPTY_L, WHITE
from settings.window_settings import HALF_SCREEN_W, SCREEN_H
from settings.UI_setings.menus_settings.multiplayer import MULTIPLAYER_BUTTONS, SERVER_PASSWORD, IP_VALUE,\
    P_NUM, PLAYER_NUMBER
from pygame.draw import line as DrawLine


class Multiplayer(MenuUI):
    def __init__(self):
        super().__init__(buttons=MULTIPLAYER_BUTTONS)
        self.create_buttons()
        self._exit_warning = False
        self._fade_surface = self.get_surface(transparent=True)
        self._fade_surface.fill(HALF_EMPTY_L)
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
        IP_VALUE.draw(dx, dy)
        P_NUM.draw(dx, dy)
        PLAYER_NUMBER.draw(dx, dy)

        DrawLine(self.surface, WHITE, (HALF_SCREEN_W, 0), (HALF_SCREEN_W, SCREEN_H), 2)

    def _update(self):
        pass


MULTIPLAYER_UI = Multiplayer()
